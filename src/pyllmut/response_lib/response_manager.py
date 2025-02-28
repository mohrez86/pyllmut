from typing import List, Dict

from .model_response_parser import ModelResponseParser


# TODO: The following method must be tested to see what happens if
#  model returns Json strings that have strings in it as
#  it already stores the code line within
#  double quotes.
def extract_mutant_dict_list(result_content: str) -> List[Dict]:
    """
    Extracts a list of mutant dictionaries from the model's response.

    This function parses the result content, which may contain arbitrary data along with a JSON string,
    and extracts the mutant data from the JSON portion. Each mutant is represented as a dictionary with
    the following structure:

        mutant_dict = {
            "pre_code": pre_code,   # The original code before mutation.
            "after_code": after_code, # The mutated code.
        }

    Args:
        result_content (str): The response returned by the model, which includes a JSON string
                              containing mutant data.

    Returns:
        List[Dict]: A list of dictionaries, where each dictionary contains "pre_code" and "after_code"
                    representing a mutant.
    """
    result_parser = ModelResponseParser(result_content)
    mutant_list = result_parser.extract_mutant_dict_list()
    return mutant_list
