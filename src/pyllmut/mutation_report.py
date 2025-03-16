from typing import List

from .mutant_lib.mutant_info import MutantInfo
from .mutant_lib.mutant_type import MutantType
from .mutant_lib.prompt_info import PromptInfo
from .mutant_lib.response_info import ResponseInfo


class MutationReport:
    """
    A report object that encapsulates the results of a mutant generation process.
    """

    def __init__(
            self,
            mutant_list: List[MutantInfo],
            timeout_info_list: List[PromptInfo],
            bad_response_info_list: List[ResponseInfo]
    ):
        """
        Initializes a MutationReport with a list of generated mutants.

        Args:
            mutant_list (List[MutantInfo]): A list of MutantInfo objects representing the generated mutants.
            timeout_info_list (List[PromptInfo]): A list of PromptInfo objects for mutant generation attempts (for a line) that timed out.
            bad_response_info_list (List[ResponseInfo]): A list of ResponseInfo objects for mutant generation attempts (for a line) that model response is not parsable (bad JSON objects).
        """
        self._mutant_list = mutant_list
        self._timeout_info_list = timeout_info_list
        self._bad_response_info_list = bad_response_info_list

    def get_mutant_list(self) -> List[MutantInfo]:
        """
        Retrieves the complete list of generated mutants.

        Returns:
            List[MutantInfo]: A list of all MutantInfo objects.
        """
        return self._mutant_list

    def get_valid_mutant_list(self) -> List[MutantInfo]:
        """
        Returns only the valid mutants from the complete mutant list.
        A mutant is considered valid if its mutant type is equal to `MutantType.VALID`.

        Returns:
            List[MutantInfo]: A list of valid MutantInfo objects.
        """
        valid_mutant_list = [x for x in self._mutant_list
                             if x.get_mutant_type() == MutantType.VALID]

        return valid_mutant_list

    def get_timeout_info_list(self) -> List[PromptInfo]:
        """
        Retrieves the list of PromptInfo objects for mutant generation attempts (for a line) that timed out.

        Returns:
            List[PromptInfo]: A list of PromptInfo objects.
        """
        return self._timeout_info_list

    def get_bad_response_info_list(self) -> List[ResponseInfo]:
        """
        Retrieves the list of ResponseInfo objects for mutant generation attempts (for a line) that model response is not parsable (bad JSON objects).

        Returns:
            List[ResponseInfo]: A list of ResponseInfo objects.
        """
        return self._bad_response_info_list
