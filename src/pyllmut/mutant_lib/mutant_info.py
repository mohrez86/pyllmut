from .mutant_type import MutantType
from .response_info import ResponseInfo


class MutantInfo(ResponseInfo):
    """
    Represents a mutation.
    """

    def __init__(
        self,
        prompt_content: str,
        original_module_content: str,
        line_number: int,
        sent_token_count: int,
        response_content: str,
        received_token_count: int,
        mutated_module_content: str,
        diff_content: str,
        pre_code_model: str,
        after_code_model: str,
        pre_code_refined: str,
        after_code_refined: str,
    ):
        """
        Initializes a Mutant instance.

        Args:
            prompt_content (str): The content of the prompt.
            original_module_content (str): The original content of the module before mutation.
            line_number (int): The line number where the mutation was applied.
            sent_token_count (int): The number of sent tokens when using the LLM.
            response_content (str): The response returned from the model.
            received_token_count (int): The number of tokens in the response.
            mutated_module_content (str): The content of the module after applying the mutation.
            diff_content (str): A diff representation of the changes between the original and mutated code.
            pre_code_model (str): The content of the line before mutation, as returned by the model.
            after_code_model (str): The content of the line after mutation, as returned by the model.
            pre_code_refined (str): The actual content of the line before mutation, extracted from the original code.
            after_code_refined (str): The content of the line after mutation, with fixed indentation.
        """
        super().__init__(
            prompt_content,
            original_module_content,
            line_number,
            sent_token_count,
            response_content,
            received_token_count
        )
        self._mutated_module_content = mutated_module_content
        self._diff_content = diff_content
        self._pre_code_model = pre_code_model
        self._after_code_model = after_code_model
        self._pre_code_refined = pre_code_refined
        self._after_code_refined = after_code_refined
        self._mutant_type = MutantType.UNKNOWN

    def __str__(self):
        return self._after_code_model

    def __repr__(self):
        return self._after_code_model

    def get_mutated_module_content(self) -> str:
        """
        Returns the content of the module after applying the mutation.

        Returns:
            str: The mutated module content.
        """
        return self._mutated_module_content

    def get_diff_content(self) -> str:
        """
        Returns a diff representation of the changes between the original and mutated code.

        Returns:
            str: The diff content.
        """
        return self._diff_content

    def get_pre_code_model(self) -> str:
        """
        Returns the content of the line before mutation, as returned by the model.

        Returns:
            str: The pre-mutation code content from the model.
        """
        return self._pre_code_model

    def get_after_code_model(self) -> str:
        """
        Returns the content of the line after mutation, as returned by the model.

        Returns:
            str: The post-mutation code content from the model.
        """
        return self._after_code_model

    def get_pre_code_refined(self) -> str:
        """
        Returns the actual content of the line before mutation, extracted from the original code.

        Returns:
            str: The refined pre-mutation code content.
        """
        return self._pre_code_refined

    def get_after_code_refined(self) -> str:
        """
        Returns the content of the line after mutation, with fixed indentation.

        Returns:
            str: The refined post-mutation code content.
        """
        return self._after_code_refined

    def get_mutant_type(self) -> MutantType:
        """
        Returns the type of the mutant.

        Returns:
            MutantType: The type of the mutant.
        """
        return self._mutant_type

    def set_mutant_type(self, mutant_type: MutantType):
        """
        Sets the type of the mutant (used during mutant classification).

        Args:
            mutant_type (MutantType): The mutant type to set.
        """
        self._mutant_type = mutant_type
