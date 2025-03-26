from .gpt_4o import Gpt4o
from .gpt_4o_mini import Gpt4oMini
from .model_base import ModelBase
from .model_type import ModelType


def get_model(
        model_type: ModelType,
        timeout_seconds: int
) -> ModelBase:
    """
    Creates and returns an instance of the Gpt4oMini model with a specified timeout.

    Args:
        model_type (ModelType): The type of model to instantiate.
        timeout_seconds (int): The number of seconds to wait before timing out the request.

    Returns:
        ModelBase: An instance of the Gpt4oMini model configured with the provided timeout.
    """
    if model_type == ModelType.GPT4oMini:
        model = Gpt4oMini(timeout_seconds=timeout_seconds)
    elif model_type == ModelType.GPT4o:
        model = Gpt4o(timeout_seconds=timeout_seconds)
    else:
        raise ValueError(f"Invalid model type: {model_type}")

    return model
