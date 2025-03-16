from abc import ABC, abstractmethod

from typing_extensions import override

from .model_response import ModelResponse


class ModelBase(ABC):
    """
    An abstract base class that defines the common interface for models.
    """

    @abstractmethod
    def invoke_prompt(self, prompt: str) -> ModelResponse:
        """
        Sends a prompt to the model and returns the response as a ModelResponse object.

        Args:
            prompt (str): The prompt to be processed by the model.

        Returns:
            ModelResponse: An object containing the model's response text,
            the number of input tokens (sent tokens),
            and the number of output tokens (received tokens).
        """
        pass

    @override
    def __str__(self):
        return "Model object"
