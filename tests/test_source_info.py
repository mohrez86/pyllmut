import sys

import pytest

from pyllmut.source_lib import source_manager
from . import utils
from .utils import get_cookiecutter_1_generate_py, get_cookiecutter_1_generate_context_dict


def test_get_code_line_context_empty_func():
    line_number = 1
    module_content = """
def func1():
    pass
""".strip()

    expected = """
def func1():
    pass
""".strip()

    actual = source_manager.get_code_line_context(module_content, line_number)
    assert actual == expected


def test_get_code_line_context_empty_line():
    line_number = 2
    module_content = """
    
def func1():
    pass
"""

    with pytest.raises(ValueError) as exc_info:
        source_manager.get_code_line_context(module_content, line_number)

    assert str(exc_info.value) == f"Line {line_number} is not a code line."


def test_get_code_line_context_cookiecutter_1_generate_py_1():
    module_ast, module_content = get_cookiecutter_1_generate_py()
    line_number = 2

    expected = '''"""Functions for generating a project from a project template."""
import fnmatch
import json
import logging
import os'''

    actual = source_manager.get_code_line_context(module_content, line_number)
    assert actual == expected


def test_get_code_line_context_cookiecutter_1_generate_py_2():
    module_ast, module_content = get_cookiecutter_1_generate_py()
    line_number = 18

    expected = '''    ContextDecodingException,
    FailedHookException,
    NonTemplatedInputDirException,
    OutputDirExistsException,
    UndefinedVariableInTemplate,
)
from cookiecutter.find import find_template'''

    actual = source_manager.get_code_line_context(module_content, line_number)
    assert actual == expected


def test_get_code_line_context_cookiecutter_1_generate_py_3():
    module_ast, module_content = get_cookiecutter_1_generate_py()
    line_number = 39

    expected = '''def is_copy_only_path(path, context):
    """Check whether the given `path` should only be copied and not rendered.

    Returns True if `path` matches a pattern in the given `context` dict,
    otherwise False.

    :param path: A file-system path referring to a file or dir that
        should be rendered or just copied.
    :param context: cookiecutter context.
    """
    try:
        for dont_render in context['cookiecutter']['_copy_without_render']:
            if fnmatch.fnmatch(path, dont_render):
                return True
    except KeyError:
        return False

    return False'''

    actual = source_manager.get_code_line_context(module_content, line_number)
    assert actual == expected


def test_get_code_line_context_cookiecutter_1_generate_py_extensive():
    # TODO: Manually checked until line 114.

    module_ast, module_content = get_cookiecutter_1_generate_py()
    context_dict = get_cookiecutter_1_generate_context_dict()

    all_code_lines = [
        2, 3, 4, 5, 6, 7, 9, 10, 11, 13, 14, 15,
        16, 17, 18, 19, 20, 21, 22, 23, 25, 28,
        38, 39, 40, 41, 42, 43, 45, 48, 50, 51,
        53, 55, 57, 59, 63, 64, 65, 67, 70, 71,
        72, 82, 84, 85, 86, 87, 90, 91, 92, 93,
        94, 95, 96, 99, 100, 101, 105, 106, 107,
        108, 110, 111, 114, 135, 138, 140, 141,
        142, 143, 144, 146, 147, 148, 150, 153,
        154, 155, 156, 157, 160, 163, 164, 165,
        168, 169, 170, 174, 175, 178, 179, 180,
        181, 183, 185, 186, 189, 192, 193, 194,
        196, 197, 199, 201, 202, 203, 205, 207,
        208, 209, 210, 211, 212, 213, 214, 215,
        216, 218, 221, 223, 224, 225, 226, 229,
        230, 231, 241, 242, 243, 244, 245, 246,
        247, 248, 249, 250, 251, 252, 255, 256,
        257, 258, 259, 260, 261, 262, 272, 273,
        274, 276, 277, 278, 279, 280, 281, 282,
        283, 284, 285, 294, 295, 299, 301, 302,
        303, 304, 306, 307, 309, 313, 314, 316,
        317, 321, 322, 323, 324, 326, 327, 328,
        329, 330, 331, 335, 336, 337, 338, 339,
        340, 341, 342, 343, 344, 345, 346, 347,
        349, 350, 351, 352, 353, 354, 355, 356,
        357, 358, 359, 360, 361, 362, 363, 364,
        365, 366, 367, 368, 369, 371, 372, 373,
        374, 375, 376, 377, 378, 380]

    for line_number in all_code_lines:
        current_expected = context_dict[str(line_number)]
        current_actual = source_manager.get_code_line_context(module_content, line_number)
        # print("\n")
        # print(f"For line number {line_number}: ")
        # print(current_actual)
        # print(f"For line number {line_number}: ")
        assert current_actual == current_expected


def test_is_code_line_simple():
    line_number = 1
    module_content = '''
def func1():
    """Some docstring"""
    pass
'''.strip()

    is_code_line = source_manager.is_code_line(module_content, line_number)
    assert is_code_line is True

    line_number = 2
    module_content = '''
def func1():
    """Some docstring"""
    pass
'''.strip()

    is_code_line = source_manager.is_code_line(module_content, line_number)
    assert is_code_line is False

    line_number = 4
    module_content = '''
def func1():
    """
    Some docstring
    another line of docstring
    one more line of docstring
    """
    pass
'''.strip()

    is_code_line = source_manager.is_code_line(module_content, line_number)
    assert is_code_line is False

    line_number = 1
    module_content = '''
def func1():
    """Some docstring"""
    pass
'''

    is_code_line = source_manager.is_code_line(module_content, line_number)
    assert is_code_line is False

    line_number = 4
    module_content = '''
def func1():
    """Some docstring"""
    # Comment line
    pass
'''

    is_code_line = source_manager.is_code_line(module_content, line_number)
    assert is_code_line is False


def test_is_code_line_cookiecutter_1_generate_py():
    module_ast, module_content = get_cookiecutter_1_generate_py()
    module_line_list = module_content.splitlines()

    expected_code_lines = [
        2, 3, 4, 5, 6, 7, 9, 10, 11, 13, 14, 15,
        16, 17, 18, 19, 20, 21, 22, 23, 25, 28,
        38, 39, 40, 41, 42, 43, 45, 48, 50, 51,
        53, 55, 57, 59, 63, 64, 65, 67, 70, 71,
        72, 82, 84, 85, 86, 87, 90, 91, 92, 93,
        94, 95, 96, 99, 100, 101, 105, 106, 107,
        108, 110, 111, 114, 135, 138, 140, 141,
        142, 143, 144, 146, 147, 148, 150, 153,
        154, 155, 156, 157, 160, 163, 164, 165,
        168, 169, 170, 174, 175, 178, 179, 180,
        181, 183, 185, 186, 189, 192, 193, 194,
        196, 197, 199, 201, 202, 203, 205, 207,
        208, 209, 210, 211, 212, 213, 214, 215,
        216, 218, 221, 223, 224, 225, 226, 229,
        230, 231, 241, 242, 243, 244, 245, 246,
        247, 248, 249, 250, 251, 252, 255, 256,
        257, 258, 259, 260, 261, 262, 272, 273,
        274, 276, 277, 278, 279, 280, 281, 282,
        283, 284, 285, 294, 295, 299, 301, 302,
        303, 304, 306, 307, 309, 313, 314, 316,
        317, 321, 322, 323, 324, 326, 327, 328,
        329, 330, 331, 335, 336, 337, 338, 339,
        340, 341, 342, 343, 344, 345, 346, 347,
        349, 350, 351, 352, 353, 354, 355, 356,
        357, 358, 359, 360, 361, 362, 363, 364,
        365, 366, 367, 368, 369, 371, 372, 373,
        374, 375, 376, 377, 378, 380]

    for line_index in range(len(module_line_list)):
        line_number = line_index + 1
        is_code_line = source_manager.is_code_line(module_content, line_number)
        assert is_code_line == (line_number in expected_code_lines)


def test_get_comments_removed():
    input_str = "x = 'abc # xyz' # something"
    expected = "x = 'abc # xyz' "
    actual = source_manager.get_comments_removed(input_str, 1, input_str)
    assert expected == actual

def test_get_comments_removed_empty():
    input_str = ""
    expected = ""
    actual = source_manager.get_comments_removed(input_str, 1, input_str)
    assert expected == actual

def test_get_comments_removed_1():
    input_str = "c = a + b"
    expected = "c = a + b"
    actual = source_manager.get_comments_removed(input_str, 1, input_str)
    assert expected == actual

    input_str = 'c = a + b'
    expected = "c = a + b"
    actual = source_manager.get_comments_removed(input_str, 1, input_str)
    assert expected == actual

    input_str = "c = a + b # something"
    expected = "c = a + b "
    actual = source_manager.get_comments_removed(input_str, 1, input_str)
    assert expected == actual

    input_str = "c = a + b # something else"
    expected = "c = a + b "
    actual = source_manager.get_comments_removed(input_str, 1, input_str)
    assert expected == actual

    input_str = "x = 'abc # xyz'"
    expected = "x = 'abc # xyz'"
    actual = source_manager.get_comments_removed(input_str, 1, input_str)
    assert expected == actual

    input_str = "x = 'abc # xyz' # something"
    expected = "x = 'abc # xyz' "
    actual = source_manager.get_comments_removed(input_str, 1, input_str)
    assert expected == actual

    input_str = "x = 'abc # xyz x/y/z'"
    expected = "x = 'abc # xyz x/y/z'"
    actual = source_manager.get_comments_removed(input_str, 1, input_str)
    assert expected == actual

    input_str = "x = 'abc # xyz x/y/z' # something"
    expected = "x = 'abc # xyz x/y/z' "
    actual = source_manager.get_comments_removed(input_str, 1, input_str)
    assert expected == actual

# def test__remove_comments_2():
#     input_str = "x = 'abc # xyz \n\r\t'"
#     expected = "x = 'abc # xyz \n\r\t'"
#     actual = MutantClassifier._remove_comments(input_str)
#     assert expected == actual
#
# def test__remove_comments_3():
#     input_str = "x = 'abc # xyz \n\r\t' # something"
#     expected = "x = 'abc # xyz \n\r\t' "
#     actual = MutantClassifier._remove_comments(input_str)
#     assert expected == actual

@pytest.mark.skipif(sys.platform != "darwin", reason="Only runs on macOS")
def test_get_comments_removed_4():
    input_str = "x = 'abc # xyz' # something \n\r\t"
    expected = "x = 'abc # xyz' "
    actual = source_manager.get_comments_removed(input_str, 1, input_str)
    assert expected == actual

def test_get_comments_removed_5():
    input_str = "copy_dirs = ['']"
    expected = "copy_dirs = ['']"
    actual = source_manager.get_comments_removed(input_str, 1, input_str)
    assert expected == actual

def test_get_comments_removed_6_1():
    input_str = "copy_dirs = []"
    expected = "copy_dirs = []"
    actual = source_manager.get_comments_removed(input_str, 1, input_str)
    assert expected == actual

def test_get_comments_removed_6_2():
    input_str = "copy_dirs = []"
    expected = "copy_dirs = []"
    actual = source_manager.get_comments_removed(input_str, 1, input_str)
    assert expected == actual

def test_get_comments_removed_7():
    module_content = """from cookiecutter.exceptions import (  # Some comment
    ContextDecodingException,
    FailedHookException,
    NonTemplatedInputDirException,
    OutputDirExistsException,
    UndefinedVariableInTemplate,
)"""
    input_str = "from cookiecutter.exceptions import (  # Some comment"
    expected = "from cookiecutter.exceptions import (  "
    actual = source_manager.get_comments_removed(module_content, 1, input_str)
    assert expected == actual

def test_get_comments_removed_8():
    module_content = utils.get_cookiecutter_1_generate_py_path().read_text()
    input_str = "    return project_dir  # Some comment"
    expected = "    return project_dir  "
    actual = source_manager.get_comments_removed(module_content, 380, input_str)
    assert expected == actual
