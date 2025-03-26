from typing import Optional
from openai import OpenAI
from typing_extensions import override
from .model_base import ModelBase
from .model_response import ModelResponse


class Gpt4o(ModelBase):
    """A wrapper class for interacting with the GPT-4o model."""

    def __init__(self, timeout_seconds: int, api_key: Optional[str] = None):
        """Initializes the Gpt4o model instance.

        Args:
            timeout_seconds: The number of seconds to wait before timing out the request.
            api_key: An optional API key for authentication. If not provided,
                the default OpenAI client configuration is used.
        """
        self._model_name = "gpt-4o"
        self._timeout_seconds = timeout_seconds
        self._api_key = api_key

    @override
    def __str__(self):
        return self._model_name

    @override
    def invoke_prompt(self, prompt: str) -> ModelResponse:
        """Sends a prompt to the model and returns the response as a ModelResponse object.

        Args:
            prompt: The input prompt string to be processed by the model.

        Returns:
            ModelResponse: An object containing the model's response text,
            the number of input tokens (sent tokens),
            and the number of output tokens (received tokens).

        Raises:
            openai.OpenAIError: If there is an error during API interaction.
        """
        client = OpenAI() if self._api_key is None else OpenAI(api_key=self._api_key)

        completion = client.chat.completions.create(
            timeout=self._timeout_seconds,
            model=self._model_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        response_text = completion.choices[0].message.content
        sent_tokens_count = completion.usage.prompt_tokens
        received_tokens_count = completion.usage.completion_tokens

        model_response = ModelResponse(
            response_text,
            sent_tokens_count,
            received_tokens_count
        )

        return model_response
