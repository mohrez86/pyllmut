from typing import Optional

from openai import OpenAI
from typing_extensions import override

from .model_base import ModelBase


class Gpt4oMini(ModelBase):
    """A wrapper class for interacting with the GPT-4o Mini model."""

    def __init__(self, api_key: Optional[str] = None):
        """Initializes the Gpt4oMini model instance.

        Args:
            api_key: An optional API key for authentication. If not provided,
                the default OpenAI client configuration is used.
        """
        self._model_name = "gpt-4o-mini"
        self._api_key = api_key

    @override
    def __str__(self):
        return self._model_name

    @override
    def invoke_prompt(self, prompt: str) -> str:
        """Sends a prompt to the model and returns the response.

        Args:
            prompt: The input prompt string to be processed by the model.

        Returns:
            str: The generated response from the model.

        Raises:
            openai.OpenAIError: If there is an error during API interaction.
        """
        client = OpenAI() if self._api_key is None else OpenAI(api_key=self._api_key)

        completion = client.chat.completions.create(
            timeout=10,  # Set timeout in seconds
            model=self._model_name,
            messages=[
                # {"role": "system", "content": "You are an expert in software engineering and programming. Your task is to assist with mutation analysis by generating mutants for given programs. Mutants are modified versions of a program created by making small syntactic changes to test the effectiveness of software tests."},
                {"role": "system", "content": "You are a helpful assistant."},
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return completion.choices[0].message.content
