import ast
from typing import List

from .mutant_info import MutantInfo
from .mutant_type import MutantType
from ..source_lib import source_manager
from ..source_lib.comment_remover import BadNewContentException


class MutantClassifier:
    """
    An in-place classifier that categorizes mutants by assigning types to them.
    """

    def __init__(self, mutant_list: List[MutantInfo]):
        """
        Initializes the classifier.

        Args:
            mutant_list (List[MutantInfo]): List of Mutant objects to classify.
        """
        self._mutant_list = mutant_list

    def classify(self):
        """
        Classifies mutants by filtering invalid ones and assigning appropriate types.
        """
        passed_list = self._filter_wrong_report(self._mutant_list)
        passed_list = self._filter_unparsable(passed_list)
        passed_list = self._filter_unchanged(passed_list)
        passed_list = self._filter_duplicate(passed_list)

        # Identifying VALID mutants
        for item in passed_list:
            item.set_mutant_type(MutantType.VALID)

    def _filter_wrong_report(self, initial_list):
        """
        Filters out mutants where the model's result is incorrect.

        Args:
            initial_list (List[MutantInfo]): List of mutants to filter.

        Returns:
            List[MutantInfo]: Filtered list of mutants.
        """

        # Remove comments.
        # Strip both of them from right and left (model is allowed to make mistakes about indentations).
        # Compare. They must be equal to pass the filter.
        passed_list = []
        for x in initial_list:
            try:
                pre_code_model_no_comments = self._remove_comments(
                    x.get_original_module_content(),
                    x.get_line_number(),
                    x.get_pre_code_model()
                ).strip()
            except BadNewContentException:
                # If pre_code_model results in tokenization error, then
                # it is definitely a wrong one (assuming the original
                # module has no error)
                continue

            pre_code_refined_no_comments = self._remove_comments(
                x.get_original_module_content(),
                x.get_line_number(),
                x.get_pre_code_refined()
            ).strip()

            if self._code_line_string_equality(
                    pre_code_model_no_comments,
                    pre_code_refined_no_comments
            ):
                passed_list.append(x)

        # passed_list = [
        #     x for x in initial_list
        #     if self._code_line_string_equality(
        #         self._remove_comments(x.get_original_module_content(), x.get_line_number(), x.get_pre_code_model()).strip(),
        #         self._remove_comments(x.get_original_module_content(), x.get_line_number(), x.get_pre_code_refined()).strip()
        #     )
        # ]

        # Filtering WRONG_REPORT mutants
        for item in initial_list:
            if item not in passed_list:
                item.set_mutant_type(MutantType.WRONG_REPORT)

        return passed_list

    def _filter_unparsable(self, initial_list):
        """
        Filters out mutants that are not syntactically valid.

        Args:
            initial_list (List[MutantInfo]): List of mutants to filter.

        Returns:
            List[MutantInfo]: Filtered list of mutants.
        """
        passed_list = [x for x in initial_list
                                if self._is_parsable(x)]

        # Filtering UNPARSABLE mutants
        for item in initial_list:
            if item not in passed_list:
                item.set_mutant_type(MutantType.UNPARSABLE)

        return passed_list

    def _filter_unchanged(self, initial_list):
        """
        Filters out mutants that remain unchanged after mutation.

        Args:
            initial_list (List[MutantInfo]): List of mutants to filter.

        Returns:
            List[MutantInfo]: Filtered list of mutants.
        """

        # Remove comments.
        # Strip both of them from right (left is not needed as they should already have the same indentation).
        # Compare. They must be different to pass the filter.
        passed_list = [
            x for x in initial_list
            if not self._code_line_string_equality(
                self._remove_comments(x.get_original_module_content(), x.get_line_number(), x.get_pre_code_refined()).rstrip(),
                self._remove_comments(x.get_original_module_content(), x.get_line_number(), x.get_after_code_refined()).rstrip()
            )
        ]

        # Filtering UNCHANGED mutants
        for item in initial_list:
            if item not in passed_list:
                item.set_mutant_type(MutantType.UNCHANGED)

        return passed_list

    def _filter_duplicate(self, initial_list):
        """
        Filters out duplicate mutants.

        Args:
            initial_list (List[MutantInfo]): List of mutants to filter.

        Returns:
            List[MutantInfo]: Filtered list of unique mutants.
        """
        passed_list = self._get_unique_mutant_list(initial_list)

        # Filtering DUPLICATE mutants
        for item in initial_list:
            if item not in passed_list:
                item.set_mutant_type(MutantType.DUPLICATE)

        return passed_list

    @staticmethod
    def _is_parsable(mutant: MutantInfo) -> bool:
        """
        Checks if a given mutant's code is syntactically valid.

        Args:
            mutant (MutantInfo): Mutant object to check.

        Returns:
            bool: True if the code is parsable, False otherwise.
        """
        try:
            ast.parse(mutant.get_mutated_module_content())
            return True
        except (SyntaxError, ValueError):
            return False

    def _get_unique_mutant_list(self, mutant_list: List[MutantInfo]) -> List[MutantInfo]:
        """
        Retrieves a list of unique mutants by skipping duplicates.

        Args:
            mutant_list (List[MutantInfo]): List of mutants to process.

        Returns:
            List[MutantInfo]: List of unique mutants.
        """
        unique_mutant_list = []
        for mutant in mutant_list:
            if not self._is_mutant_in_list(mutant, unique_mutant_list):
                unique_mutant_list.append(mutant)

        return unique_mutant_list

    def _is_mutant_in_list(self, mutant: MutantInfo, mutant_list: List[MutantInfo]) -> bool:
        """
        Checks if a mutant already exists in the given list.

        Args:
            mutant (MutantInfo): Mutant object to check.
            mutant_list (List[MutantInfo]): List of existing mutants.

        Returns:
            bool: True if the mutant is found, False otherwise.
        """
        for item in mutant_list:
            if self._is_equal_mutant(item, mutant):
                return True
        return False

    def _is_equal_mutant(self, mutant_1: MutantInfo, mutant_2: MutantInfo) -> bool:
        """
        Checks if two mutants are identical.

        Args:
            mutant_1 (MutantInfo): First mutant.
            mutant_2 (MutantInfo): Second mutant.

        Returns:
            bool: True if both mutants are identical, False otherwise.
        """
        if (
                mutant_1.get_original_module_content() == mutant_2.get_original_module_content()
                and mutant_1.get_line_number() == mutant_2.get_line_number()

                # Remove comments.
                # Strip both of them from right (left is not needed; indentation must already be the same)
                # Compare.
                and self._code_line_string_equality(
                                                        self._remove_comments(
                                                            mutant_1.get_original_module_content(),
                                                            mutant_1.get_line_number(),
                                                            mutant_1.get_after_code_refined()
                                                        ).rstrip(),
                                                        self._remove_comments(
                                                            mutant_2.get_original_module_content(),
                                                            mutant_2.get_line_number(),
                                                            mutant_2.get_after_code_refined()
                                                        ).rstrip()
                                                    )
        ):
            assert mutant_1.get_pre_code_refined() == mutant_2.get_pre_code_refined()
            return True

        return False

    @staticmethod
    def _remove_comments(module_content: str, line_number: int, code_line: str) -> str:
        """Removes comments from a given line of code.

        Args:
            module_content (str): The complete source code of the module.
            line_number (int): Code line number whose comment is supposed to be removed.
            code_line (str): The content of the line whose comment is supposed to be removed.

        Returns:
            str: The code line with comments removed.
        """
        return source_manager.get_comments_removed(module_content, line_number, code_line)


    @staticmethod
    def _code_line_string_equality(code_line_1: str, code_line_2: str) -> bool:
        """Compares two code lines of Python code for equality.

        Treats single and double quotes as equivalent.

        Args:
            code_line_1 (str): The first code line to compare.
            code_line_2 (str): The second code line to compare.

        Returns:
            bool: True if the lines are considered equal, False otherwise.
        """
        return (code_line_1 == code_line_2 or
                code_line_1.replace("'", '"') == code_line_2.replace("'", '"'))
