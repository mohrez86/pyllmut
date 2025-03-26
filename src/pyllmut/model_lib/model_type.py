from enum import Enum

class ModelType(Enum):
    """Enum representing different model types supported by PyLLMut.

    Attributes:
        GPT4oMini (int): Represents the 'GPT-4o mini' model.
        GPT4o (int): Represents the 'gpt-4o' model.
    """

    GPT4oMini = 1
    GPT4o = 2
