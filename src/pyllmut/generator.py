import logging
from typing import List, Optional, Tuple

import openai

from .model_lib.model_type import ModelType
from .model_lib import model_manager
from .mutant_lib import mutant_manager
from .mutant_lib.mutant_info import MutantInfo
from .mutant_lib.prompt_info import PromptInfo
from .mutant_lib.response_info import ResponseInfo
from .mutation_report import MutationReport
from .prompt_lib import prompt_manager
from .response_lib import response_manager
from .source_lib import source_manager

logger = logging.getLogger(__name__)


class MutantGenerator:
    """
    A class for generating mutants for a given Python module.
    This class uses an LLM to generate code mutants for specified lines in a module.
    """

    def __init__(
            self,
            module_content: str,
            line_number_list: Optional[List[int]] = None,
            mutants_per_line_count: int = 1,
            timeout_seconds_per_line: int = 10,
            model_type: ModelType = ModelType.GPT4oMini
    ):
        """
        Initializes the MutantGenerator.

        Args:
            module_content (str): The content of the Python module to mutate.
            line_number_list (Optional[List[int]]): List of line numbers to generate mutants for.
                If None, mutants will be generated for all code lines.
            mutants_per_line_count (int): Desired number of mutants to generate per line.
                It must be greater than 0. However, note that the LLM may not always comply
                with this number, but it usually does.
            timeout_seconds_per_line (int): Timeout in seconds for generating mutants for a line.
                It must be greater than 0.
            model_type (ModelType): The LLM model used for mutation generation. Defaults to `GPT4oMini`.

        Raises:
            AssertionError: If `mutants_per_line_count` or `timeout_seconds_per_line` is not greater than 0.
        """
        self._module_content = module_content
        self._line_number_list = line_number_list
        self._model_type = model_type

        assert (
            mutants_per_line_count > 0
        ), "mutants_per_line_count must be greater than 0"
        self._mutants_per_line_count = mutants_per_line_count

        assert (
                timeout_seconds_per_line > 0
        ), "timeout_seconds_per_line must be greater than 0"
        self._timeout_seconds_per_line = timeout_seconds_per_line

    def generate(self) -> MutationReport:
        """
        Generates mutants for the module and returns a MutationReport.

        Returns:
            MutationReport: An object containing the mutation generation results.
        """
        module_mutant_list = []
        module_timeout_info_list = []
        module_bad_response_info_list = []

        if self._line_number_list is None:
            self._line_number_list = source_manager.get_module_code_line_list(self._module_content)

        for line_number in self._line_number_list:
            logger.info(
                f"LLM is generating {self._mutants_per_line_count} mutant(s) for line {line_number}."
            )

            # `_mutants_per_line_count` serves as a guideline for the model,
            # but it is not strictly enforced.
            # The model may generate more or fewer mutants than specified.
            # It is the responsibility of PyLLMut's client to check
            # the count and take appropriate action if needed.
            (
                line_mutant_list,
                line_timeout_info,
                line_bad_response_info
            ) = self._generate_mutant_list(line_number)

            module_mutant_list += line_mutant_list

            if line_timeout_info is not None:
                module_timeout_info_list.append(line_timeout_info)

            if line_bad_response_info is not None:
                module_bad_response_info_list.append(line_bad_response_info)

        mutant_manager.classify_mutant_list(module_mutant_list)

        mutation_report = MutationReport(module_mutant_list, module_timeout_info_list, module_bad_response_info_list)

        return mutation_report

    def _generate_mutant_list(
            self,
            line_number: int
    ) -> Tuple[List[MutantInfo], Optional[PromptInfo], Optional[ResponseInfo]]:
        """
        Generates mutants for a specific line in the Python module.

        Args:
            line_number (int): The line number to generate mutants for.

        Returns:
            List[MutantInfo]: A list of MutantInfo objects generated for the specified line.
        """

        # We only generate mutants for code lines.
        if not source_manager.is_code_line(self._module_content, line_number):
            logger.info(f"Line {line_number} is not a code line, and thus, no mutants are generated for it.")
            return [], None, None

        code_line_context = source_manager.get_code_line_context(
            self._module_content, line_number
        )
        code_line = source_manager.get_code_line(self._module_content, line_number)
        prompt_content = prompt_manager.get_prompt(
            code_line_context, self._mutants_per_line_count, code_line
        )

        model = model_manager.get_model(
            self._model_type,
            self._timeout_seconds_per_line
        )

        logger.info(f"PyLLMut is using model {model}.")

        try:
            model_response = model.invoke_prompt(prompt_content)
        except openai.APITimeoutError:
            timeout_info = PromptInfo(prompt_content, self._module_content, line_number)
            return [], timeout_info, None

        try:
            mutant_dict_list = response_manager.extract_mutant_dict_list(
                model_response.get_response_content()
            )
        except ValueError:
            bad_response_info = ResponseInfo(
                prompt_content,
                self._module_content,
                line_number,
                model_response.get_sent_token_count(),
                model_response.get_response_content(),
                model_response.get_received_token_count()
            )
            return [], None, bad_response_info

        mutant_list = []
        for mutant_dict in mutant_dict_list:
            mutant = mutant_manager.get_mutant(
                prompt_content,
                model_response.get_response_content(),
                model_response.get_sent_token_count(),
                model_response.get_received_token_count(),
                self._module_content,
                line_number,
                mutant_dict,
            )
            mutant_list.append(mutant)

        return mutant_list, None, None
