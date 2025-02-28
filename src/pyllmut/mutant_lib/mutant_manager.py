from typing import Dict, List

from .mutant_info import MutantInfo
from .mutant_builder import MutantBuilder
from .mutant_classifier import MutantClassifier


def get_mutant(
        module_content: str,
        line_number: int,
        mutant_dict: Dict) -> MutantInfo:
    """Creates and returns a Mutant object based on the mutant dictionary.

    Args:
        module_content (str): The content of the module as a string.
        line_number (int): The line number in the module where the mutation occurs.
        mutant_dict (Dict): A dictionary containing 'pre_code' and 'after_code' representing the mutant.

    Returns:
        MutantInfo: A Mutant object that represents the mutation.
    """
    pre_code_model = mutant_dict["pre_code"]
    after_code_model = mutant_dict["after_code"]
    mutant_builder = MutantBuilder(module_content, line_number, pre_code_model, after_code_model)
    mutant = mutant_builder.build()

    return mutant


def classify_mutant_list(mutant_list: List[MutantInfo]):
    """Classifies a list of mutants by updating their `_mutant_type` attribute in place.

    Args:
        mutant_list (List[MutantInfo]): A list of MutantInfo objects to be classified.
    """
    mutant_classifier = MutantClassifier(mutant_list)
    mutant_classifier.classify()
