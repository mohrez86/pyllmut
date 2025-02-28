import logging
from typing import List, Optional

from .model_lib import model_manager
from .mutant_lib import mutant_manager
from .mutant_lib.mutant_info import MutantInfo
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
            mutants_per_line_count: int = 1
    ):
        """
        Initializes the MutantGenerator.

        Args:
            module_content (str): The content of the Python module to mutate.
            line_number_list (Optional[List[int]]): List of line numbers to generate mutants for.
                If None, mutants will be generated for all code lines.
            mutants_per_line_count (int): Desired number of mutants to generate per line.
                Must be greater than 0. However, note that the LLM model may not always comply
                with this number, but it usually does.

        Raises:
            AssertionError: If mutants_per_line_count is not greater than 0.
        """
        self._module_content = module_content
        self._line_number_list = line_number_list

        assert (
            mutants_per_line_count > 0
        ), "mutants_per_line_count must be greater than 0"

        self._mutants_per_line_count = mutants_per_line_count

    def generate(self) -> MutationReport:
        """
        Generates mutants for the module and returns a MutationReport.
        If no specific line numbers are provided, mutants are generated for all code lines.

        Returns:
            MutationReport: An object containing a list of generated MutantInfo objects.
        """
        module_mutant_list = []

        if self._line_number_list is None:
            self._line_number_list = source_manager.get_module_code_line_list(self._module_content)

        for line_number in self._line_number_list:
            logger.info(
                f"LLM is generating {self._mutants_per_line_count} mutant(s) for line {line_number}."
            )

            # TODO: `_mutants_per_line_count` is used by the model, and thus,
            #  there is no guarantee that the model complies with it. We need to check
            #  the number of generated mutants ourselves. If the count does not match
            #  our request, we must take action. Currently, if more mutants are generated
            #  than requested, we return the extras too.
            #  If fewer are generated, we return all the mutants produced without
            #  attempting to generate additional ones.
            line_mutant_list = self._generate_mutant_list(line_number)
            module_mutant_list += line_mutant_list

        mutant_manager.classify_mutant_list(module_mutant_list)

        mutation_report = MutationReport(module_mutant_list)

        return mutation_report

    def _generate_mutant_list(self, line_number: int) -> List[MutantInfo]:
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
            return []

        code_line_context = source_manager.get_code_line_context(
            self._module_content, line_number
        )
        code_line = source_manager.get_code_line(self._module_content, line_number)

        prompt = prompt_manager.get_prompt(
            code_line_context, self._mutants_per_line_count, code_line
        )

        model = model_manager.get_model_gpt_4o_mini()
        result_content = model.invoke_prompt(prompt)

        # TODO: Parsing the result can go wrong.
        #  Maybe the model did not return a json list.
        #  For now, we simply ignore the result as if
        #  the model was not able to generate any mutants
        #  for the given line number.
        #  Other strategies can be prompting the model again.
        #  Or we can ask the model to return result as JSON already.
        #  I think OpenAI supports it.
        try:
            mutant_dict_list = response_manager.extract_mutant_dict_list(
                result_content
            )
        except ValueError:
            mutant_dict_list = []

        mutant_list = []
        for mutant_dict in mutant_dict_list:
            mutant = mutant_manager.get_mutant(
                self._module_content,
                line_number,
                mutant_dict,
            )
            mutant_list.append(mutant)

        return mutant_list
