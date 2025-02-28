import ast


class CodeLineChecker:
    def __init__(self, module_content: str, line_number: int):
        self._module_content = module_content
        self._line_number = line_number
        self._module_line_list = module_content.splitlines()
        self._module_ast = ast.parse(module_content)
        self._line_content = self._module_line_list[self._line_number - 1]

    def is_code_line(self) -> bool:
        return (not self._is_empty_line() and
                not self._is_comment_line() and
                not self._is_docstring_line())

    def _is_empty_line(self) -> bool:
        return self._line_content.strip() == ""

    def _is_comment_line(self) -> bool:
        return self._line_content.strip().startswith("#")

    def _is_docstring_line(self):
        for node in ast.walk(self._module_ast):
            if self._is_docstring_node(node):
                start_line = node.lineno
                end_line = self._get_docstring_node_end_line(node)
                if start_line <= self._line_number <= end_line:
                    return True
        return False

    @staticmethod
    def _get_docstring_node_end_line(node):
        # TODO: Uncomment this before releasing.
        # # For Python versions that support `node.end_lineno`
        # if hasattr(node, "end_lineno"):
        #     return node.end_lineno

        # TODO: Needs to be checked in Python 3.6
        # For Python 3.6 that does not support `node.end_lineno`
        docstring_content = node.value.s  # Extract the docstring content
        start_line = node.lineno
        end_line = start_line + len(docstring_content.splitlines()) - 1

        # TODO: Remove this. It is only for testing.
        assert end_line == node.end_lineno

        return end_line

    @staticmethod
    def _is_docstring_node(node) -> bool:
        """Checks if the ast node is a docstring node"""

        # Python >= 3.8: docstrings are ast.Constant
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant):
            return isinstance(node.value.value, str)

        # Python <= 3.7: docstrings are ast.Str
        elif isinstance(node, ast.Expr) and isinstance(node.value, ast.Str):
            return True

        return False
