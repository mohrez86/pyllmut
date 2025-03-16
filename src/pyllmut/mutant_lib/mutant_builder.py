import difflib

from .mutant_info import MutantInfo


class MutantBuilder:
    """A class responsible for constructing a Mutant object from a mutant dictionary."""

    def __init__(
            self,
            prompt_content: str,
            response_content: str,
            sent_token_count: int,
            received_token_count: int,
            module_content: str,
            line_number: int,
            pre_code_model: str,
            after_code_model: str
    ):
        """
        Initializes the object.

        Args:
            prompt_content (str): The content of the prompt for sent to the model.
            response_content (str): The content of the response received from the model.
            sent_token_count (int): The number of tokens sent in the prompt.
            received_token_count (int): The number of tokens received in the response.
            module_content (str): The content of the module as a string.
            line_number (int): The line number in the module to apply the mutation.
            pre_code_model (str): The code line content before the mutation, returned by the model.
            after_code_model (str): The code line content after the mutation, returned by the model.
        """
        self._prompt_content = prompt_content
        self._response_content = response_content
        self._sent_token_count = sent_token_count
        self._received_token_count = received_token_count
        self._module_content = module_content
        self._line_number = line_number
        self._pre_code_model = pre_code_model
        self._after_code_model = after_code_model
        self._module_line_list = module_content.splitlines()

    def build(self) -> MutantInfo:
        """
        Builds and returns a Mutant object.

        Returns:
            MutantInfo: A Mutant object containing the original module, mutated module, and the diff between them.
        """
        line_index = self._line_number - 1

        pre_code_refined = self._module_line_list[line_index]

        ## Note that `self._pre_code_model` returned by the model can be wrong (i.e., not equal to `pre_code_refined`).
        ## Here, we do not check if the LLM report is correct or not. We do it in a filtering phase.
        # assert pre_code_refined == self._pre_code_model

        # Here, the goal is to increase the likelihood of generating parsable mutants.
        # If the model modifies the indentation as part of the mutation, we
        # ignore it because most probably it will result in an unparsable code.
        original_line_indentation = self._extract_code_line_indentation(pre_code_refined)

        after_code_refined = original_line_indentation + self._after_code_model.lstrip()
        assert after_code_refined.strip() == self._after_code_model.strip()

        mutated_module_content = self._get_mutated_module_content(line_index, after_code_refined)

        diff = difflib.unified_diff(
            self._module_content.splitlines(),
            mutated_module_content.splitlines(),
            lineterm='',  # Prevent adding extra newlines
            fromfile="original",
            tofile="modified"
        )

        diff_content = "\n".join(diff)

        mutant = MutantInfo(
            prompt_content=self._prompt_content,
            original_module_content=self._module_content,
            line_number=self._line_number,
            sent_token_count=self._sent_token_count,
            response_content=self._response_content,
            received_token_count=self._received_token_count,
            mutated_module_content=mutated_module_content,
            diff_content=diff_content,
            pre_code_model= self._pre_code_model,
            after_code_model=self._after_code_model,
            pre_code_refined=pre_code_refined,
            after_code_refined=after_code_refined
        )

        return mutant

    @staticmethod
    def _extract_code_line_indentation(line_content) -> str:
        """
        Separates the indentation (spaces/tabs) from the actual code content in a line of code.

        Args:
            line_content (str): The line of code whose indentation is to be extracted.

        Returns:
            str: The indentation of the line.
        """
        line_length = len(line_content)
        statement_length = len(line_content.lstrip())
        statement_start_index = line_length - statement_length
        statement_content = line_content[statement_start_index:]
        indentation_content = line_content[:statement_start_index]
        assert len(indentation_content) + len(statement_content) == len(line_content)

        return indentation_content

    def _get_mutated_module_content(self, line_to_change_index, new_line_content):
        """
        Generates the mutated module content by replacing the specified line with the mutated line.

        Args:
            line_to_change_index (int): The index of the line to be mutated.
            new_line_content (str): The new content to replace the original line.

        Returns:
            str: The mutated module content.
        """
        mutated_module_line_list = []
        for line_index in range(len(self._module_line_list)):
            if line_index == line_to_change_index:
                mutated_module_line_list.append(new_line_content)
            else:
                mutated_module_line_list.append(self._module_line_list[line_index])

        # TODO: It removes the empty lines at the end of the module.
        #  Not a serious problem but fix it.
        mutated_module_content = "\n".join(mutated_module_line_list)

        return mutated_module_content
