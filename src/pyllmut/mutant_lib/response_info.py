from .prompt_info import PromptInfo


class ResponseInfo(PromptInfo):
    """A class to store information about response details from the LLM."""

    def __init__(
            self,
            prompt_content: str,
            original_module_content: str,
            line_number: int,
            sent_token_count: int,
            response_content: str,
            received_token_count: int
    ):
        """
        Initializes the ResponseInfo object with the given parameters.

        Args:
            prompt_content (str): The content of the prompt.
            original_module_content (str): The content of the module we plan to generate mutants for.
            line_number (int): The line number in the module where we want to generate mutants.
            sent_token_count (int): The number of sent tokens when using the LLM.
            response_content (str): The response returned from the model.
            received_token_count (int): The number of tokens in the response.
        """
        super().__init__(
            prompt_content,
            original_module_content,
            line_number
        )
        self._sent_token_count = sent_token_count
        self._response_content = response_content
        self._received_token_count = received_token_count

    def get_sent_token_count(self) -> int:
        """Returns the number of sent tokens when using the LLM."""
        return self._sent_token_count

    def get_response_content(self) -> str:
        """Returns the response returned from the model."""
        return self._response_content

    def get_received_token_count(self) -> int:
        """Returns the number of tokens in the response."""
        return self._received_token_count
