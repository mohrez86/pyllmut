from .gpt_4o_mini import Gpt4oMini
from .model_base import ModelBase


def get_model_gpt_4o_mini() -> ModelBase:
    """
    Creates and returns an instance of the Gpt4oMini model.

    Returns:
        ModelBase: An instance of the Gpt4oMini model.
    """
    model = Gpt4oMini()
    return model
