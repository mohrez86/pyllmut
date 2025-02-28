import ast
import io
import token
import tokenize
from typing import List


class BadNewContentException(Exception):
    """Raised when the new module content is not parsable or tokenizable."""
    pass


class CommentRemover:
    def get_comments_removed(
            self,
            module_content: str,
            line_number: int,
            line_content: str) -> str:

        if module_content == "":
            assert line_content == ""
            return line_content

        module_line_list = module_content.splitlines()
        line_index = line_number - 1

        original_indentation = self._extract_code_line_indentation(line_content)

        in_module_content = module_line_list[line_index]
        correct_indentation = self._extract_code_line_indentation(in_module_content)

        line_content_fixed = correct_indentation + line_content.lstrip()
        assert line_content_fixed.strip() == line_content.strip()
        new_module_content = self._get_new_module_content(module_line_list, line_index, line_content_fixed)

        try:
            ast.parse(new_module_content)
        except (SyntaxError, ValueError):
            raise BadNewContentException()

        module_stream = io.StringIO(new_module_content)

        try:
            module_token_list = list(tokenize.generate_tokens(module_stream.readline))
        except tokenize.TokenError:
            raise BadNewContentException()

        error_token_list = [x for x in module_token_list if x.type == token.ERRORTOKEN]
        assert len(error_token_list) == 0

        line_comment_token_list = [x for x in module_token_list if x.type == token.COMMENT and x.start[0] == line_number]
        assert 0 <= len(line_comment_token_list) <= 1

        line_content_no_comments = line_content
        if len(line_comment_token_list) > 0:
            comment_token = line_comment_token_list[0]
            start_line = comment_token.start[0]
            start_column = comment_token.start[1]
            assert start_line == line_number
            line_content_no_comments = original_indentation + new_module_content.splitlines()[line_index][0:start_column].lstrip()

        return line_content_no_comments


    @staticmethod
    def _get_new_module_content(module_line_list: List[str], line_to_change_index, new_line_content):
        """
        Generates the new module content by replacing the specified line with the new line.

        Args:
            line_to_change_index (int): The index of the line to be changed.
            new_line_content (str): The new content to replace the original line.

        Returns:
            str: The new module content as a string.
        """

        # TODO: Duplicate somewhere else.

        mutated_module_line_list = []
        for line_index in range(len(module_line_list)):
            if line_index == line_to_change_index:
                mutated_module_line_list.append(new_line_content)
            else:
                mutated_module_line_list.append(module_line_list[line_index])

        # TODO: It removes the empty lines at the end of the module.
        #  Not a serious problem but fix it.
        mutated_module_content = "\n".join(mutated_module_line_list)

        return mutated_module_content


    @staticmethod
    def _extract_code_line_indentation(line_content) -> str:
        """
        Separates the indentation (spaces/tabs) from the actual code content in a line of code.

        Args:
            line_content (str): The line of code whose indentation is to be extracted.

        Returns:
            str: A string representing the indentation of the line.
        """

        # TODO: Duplicate somewhere else.

        line_length = len(line_content)
        statement_length = len(line_content.lstrip())
        statement_start_index = line_length - statement_length
        statement_content = line_content[statement_start_index:]
        indentation_content = line_content[:statement_start_index]
        assert len(indentation_content) + len(statement_content) == len(line_content)

        return indentation_content
