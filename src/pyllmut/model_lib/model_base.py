from abc import ABC, abstractmethod

from typing_extensions import override


class ModelBase(ABC):
    """
    An abstract base class that defines the common interface for models that process
    prompts and return responses.
    """

    @abstractmethod
    def invoke_prompt(self, prompt: str) -> str:
        """
        Process a given prompt and return a corresponding response.

        Args:
            prompt (str): The prompt to be processed by the model.

        Returns:
            str: The model's response to the prompt.
        """
        pass

    @override
    def __str__(self):
        return "Model object"
