from .gpt_4o_mini import Gpt4oMini
from .model_base import ModelBase


def get_model_gpt_4o_mini(timeout_seconds: int) -> ModelBase:
    """
    Creates and returns an instance of the Gpt4oMini model with a specified timeout.

    Args:
        timeout_seconds (int): The number of seconds to wait before timing out the request.

    Returns:
        ModelBase: An instance of the Gpt4oMini model configured with the provided timeout.
    """
    model = Gpt4oMini(timeout_seconds=timeout_seconds)
    return model
