from typing import List

from .mutant_lib.mutant_info import MutantInfo
from .mutant_lib.mutant_type import MutantType


class MutationReport:
    """
    A report object that encapsulates the results of a mutant generation process.
    """

    def __init__(self, mutant_list: List[MutantInfo]):
        """
        Initializes a MutationReport with a list of generated mutants.

        Args:
            mutant_list (List[MutantInfo]): A list of MutantInfo objects representing the generated mutants.
        """
        self._mutant_list = mutant_list

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
