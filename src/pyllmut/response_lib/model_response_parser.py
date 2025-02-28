import json
import re
from typing import List, Dict


class ModelResponseParser:
    """
    A class to parse a model response and extract mutant information from it.
    """

    def __init__(self, model_result: str):
        """
        Initializes the ModelResponseParser with the model response content.

        Args:
            model_result (str): The string containing the model response.
        """
        self._model_result = model_result

    def extract_mutant_dict_list(self) -> List[Dict]:
        """
        Extracts a list of mutant dictionaries from the model response.

        Returns:
            List[Dict]: A list of dictionaries, each containing "pre_code" and "after_code" representing a mutant.

        Raises:
            ValueError: If no JSON list is found in the input string.
        """
        json_pattern = r"\[\s*\{.*?\}\s*\]"
        match = re.search(json_pattern, self._model_result, re.DOTALL)

        mutant_dict_list = []

        if match:
            # Extract the JSON string
            json_str = match.group(0)
            dict_list = json.loads(json_str)
            for dict_item in dict_list:
                pre_code = dict_item.get("precode")
                after_code = dict_item.get("aftercode")
                mutant_dict = {
                    "pre_code": pre_code,
                    "after_code": after_code,
                }
                mutant_dict_list.append(mutant_dict)
        else:
            raise ValueError("No JSON list found in the input string.")

        return mutant_dict_list
