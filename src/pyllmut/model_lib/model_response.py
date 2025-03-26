class ModelResponse:
    """Represents the response from an LLM model."""

    def __init__(
            self,
            response_text: str,
            sent_tokens_count: int,
            received_tokens_count: int
    ):
        """
        Initializes a ModelResponse instance.

        Args:
            response_text (str): The generated response text.
            sent_tokens_count (int): The number of tokens sent in the request (input tokens).
            received_tokens_count (int): The number of tokens received in the response (output tokens).
        """
        self._response_text = response_text
        self._sent_tokens_count = sent_tokens_count
        self._received_tokens_count = received_tokens_count

    def get_response_content(self) -> str:
        """Returns the generated response text.

        Returns:
            str: The response text.
        """
        return self._response_text

    def get_sent_token_count(self) -> int:
        """Returns the number of tokens in the prompt (sent tokens).

        Returns:
            int: The number of input tokens.
        """
        return self._sent_tokens_count

    def get_received_token_count(self) -> int:
        """Returns the number of tokens in the model's response (received tokens).

        Returns:
            int: The number of output tokens.
        """
        return self._received_tokens_count
