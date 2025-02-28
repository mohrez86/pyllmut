from typing import List

from .code_line_checker import CodeLineChecker
from .comment_remover import CommentRemover
from .line_context_finder import LineContextFinder


def get_module_code_line_list(module_content: str) -> List[int]:
    """
    Retrieves a sorted list of line numbers that contain code in a given module.

    Args:
        module_content (str): The content of the module as a string.

    Returns:
        List[int]: A sorted list of line numbers that contain code.
    """
    code_line_set = set()

    module_line_count = len(module_content.splitlines())
    for line_index in range(module_line_count):
        line_number = line_index + 1
        if is_code_line(module_content, line_number):
            code_line_set.add(line_number)

    code_line_list = list(code_line_set)
    code_line_list.sort()
    return code_line_list


def get_code_line(module_content: str, line_number: int) -> str:
    """
    Retrieves the specific line of code from the module content.

    Args:
        module_content (str): The content of the module as a string.
        line_number (int): The line number to retrieve.

    Returns:
        str: The code line as a string.
    """
    module_lines = module_content.splitlines()
    code_line = module_lines[line_number - 1]
    return code_line


def get_code_line_context(module_content, line_number) -> str:
    """
    Retrieves the context of a specific line in the module content.

    Args:
        module_content (str): The content of the module as a string.
        line_number (int): The line number whose context is to be retrieved.

    Returns:
        str: The context of the code line as a string.
    """
    context_finder = LineContextFinder(module_content, line_number)
    code_line_context = context_finder.get_code_line_context()
    return code_line_context


def is_code_line(module_content: str, line_number: int) -> bool:
    """
    Determines whether the given line in the module content contains code.

    Args:
        module_content (str): The content of the module as a string.
        line_number (int): The line number to check.

    Returns:
        bool: True if the line contains code, False otherwise.
    """
    code_line_checker = CodeLineChecker(module_content, line_number)
    return code_line_checker.is_code_line()


def get_comments_removed(module_content: str, line_number: int, line_content: str) -> str:
    """
    Removes comments from the specified line of code in the module content.

    Args:
        module_content (str): The content of the module as a string.
        line_number (int): The line number where the code is located.
        line_content (str): The content of the line from which to remove comments.

    Returns:
        str: The line content with comments removed.
    """
    comment_remover = CommentRemover()
    line_content_no_comments = comment_remover.get_comments_removed(module_content, line_number, line_content)
    return line_content_no_comments
