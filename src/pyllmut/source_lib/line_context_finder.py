import ast
from copy import copy
from typing import List, Dict

from .code_line_checker import CodeLineChecker


class LineContextFinder:
    """
    A class for extracting the context of a specific line in a Python module.
    """
    _Context_pre_size = 3
    _Context_post_size = 3

    def __init__(self, module_content: str, line_number: int):
        """
        Initializes the LineContextFinder.

        Args:
            module_content (str): The content of the Python module as a string.
            line_number (int): The line number for which the context should be retrieved.
        """
        self._module_content = module_content
        self._line_number = line_number
        self._module_ast = ast.parse(module_content)
        self._module_line_list = module_content.splitlines()

    def _get_function_end_line(self, func_ast_node) -> int:
        """Calculates the last line of a function."""

        # For Python versions that support `func_ast_node.end_lineno`
        if hasattr(func_ast_node, "end_lineno"):
            return func_ast_node.end_lineno

        # For Python 3.7 that does not support `func_ast_node.end_lineno`
        ending_line = self._get_function_end_line_legacy(func_ast_node)

        # if hasattr(func_ast_node, "end_lineno"):
        #     assert ending_line == func_ast_node.end_lineno

        return ending_line

    def _get_function_end_line_legacy(self, func_ast_node):
        """
        For Python 3.7 that does not support `func_ast_node.end_lineno`.
        The computed end line by this function is an approximation.
        """
        line_end_max = -1

        if hasattr(func_ast_node, "__dict__"):
            all_att = func_ast_node.__dict__
            for att in all_att:
                att_instance = func_ast_node.__getattribute__(att)
                if isinstance(att_instance, list):
                    for sub_att in att_instance:
                        line_end_max = max(self._get_function_end_line_legacy(sub_att), line_end_max)
                else:
                    line_end_max = max(
                        self._get_function_end_line_legacy(att_instance), line_end_max
                    )
                if hasattr(att_instance, "lineno"):
                    line_end_max = max(att_instance.lineno, line_end_max)

        if hasattr(func_ast_node, "lineno"):
            line_end_max = max(func_ast_node.lineno, line_end_max)
        return line_end_max

    def _get_function_info_dict_list(self) -> List[Dict]:
        """Collects information about every function within the module."""

        functions_info_dict_list = []

        for node in ast.walk(self._module_ast):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                start_line = node.lineno
                end_line = self._get_function_end_line(node)
                # end_line = utils.get_node_ending_line(node, self._module_content)
                functions_info_dict_list.append({
                    "name": node.name,
                    "start_line": start_line,
                    "end_line": end_line
                })

        return functions_info_dict_list

    def get_code_line_context(self) -> str:
        """
        Retrieves the code context surrounding a specific line.

        If the line is within a function, the entire function's code is returned.
        Otherwise, a predefined number of lines before and after the target line are included.

        Returns:
            str: The code context as a string.

        Raises:
            ValueError: If the specified line is not a code line.
        """
        if not self._is_code_line():
            raise ValueError(f"Line {self._line_number} is not a code line.")

        function_info_list = self._get_function_info_dict_list()
        func_info_list_for_line = [x for x in function_info_list
                                   if x["start_line"] <= self._line_number <= x["end_line"]]

        # If the line is inside a function
        if len(func_info_list_for_line) > 0:
            # In case of nested functions, we want the most inner function that contains the line.
            inner_func_info_for_line = min(func_info_list_for_line, key=lambda x: x["end_line"] - x["start_line"])

            func_line_start = inner_func_info_for_line["start_line"]
            func_line_end = inner_func_info_for_line["end_line"]
            function_code = "\n".join(self._module_line_list[func_line_start - 1:func_line_end])
            function_code = function_code

            return function_code

        # If the line is not inside a function
        line_index = self._line_number - 1

        start_line_index = max(0, line_index - self._Context_pre_size)
        end_line_index = min(len(self._module_line_list), line_index + self._Context_post_size)

        context_code = "\n".join(self._module_line_list[start_line_index:end_line_index + 1])

        return context_code

    def _is_code_line(self):
        return CodeLineChecker(self._module_content, self._line_number).is_code_line()
