import pytest

from pyllmut.response_lib.response_manager import extract_mutant_dict_list


def test_extract_mutant_list():
    input_result = """something ```json
[
    {
        "id": 1,
        "line": 16,
        "precode": "with open(context_file) as file_handle:",
        "filepath": "project_generator.py",
        "aftercode": "with open(context_file, 'r') as file_handle:"
    },
    {
        "id": 2,
        "line": 16,
        "precode": "with open(context_file) as file_handle:",
        "filepath": "project_generator.py",
        "aftercode": "with open(context_file, 'rb') as file_handle:"
    },
    {
        "id": 3,
        "line": 16,
        "precode": "with open(context_file) as file_handle:",
        "filepath": "project_generator.py",
        "aftercode": "with open(context_file, 'a') as file_handle:"
    },
    {
        "id": 4,
        "line": 16,
        "precode": "with open(context_file) as file_handle:",
        "filepath": "project_generator.py",
        "aftercode": "if os.path.exists(context_file): with open(context_file) as file_handle:"
    }
]
``` something
"""

    expected_result = [
        {
            'after_code': "with open(context_file, 'r') as file_handle:",
            'pre_code': 'with open(context_file) as file_handle:'
        },
        {
            'after_code': "with open(context_file, 'rb') as file_handle:",
            'pre_code': 'with open(context_file) as file_handle:'
        },
        {
            'after_code': "with open(context_file, 'a') as file_handle:",
            'pre_code': 'with open(context_file) as file_handle:'
        },
        {
            'after_code': 'if os.path.exists(context_file): with open(context_file) as file_handle:',
            'pre_code': 'with open(context_file) as file_handle:'
        }
    ]

    actual_result = extract_mutant_dict_list(input_result)
    assert actual_result == expected_result

def test_extract_mutant_list_no_matching_json():
    input_result = """something ```json
[
    {
        "id": 1,
        "line": 16,
        "precode": "with open(context_file) as file_handle:",
        "filepath": "project_generator.py",
        "aftercode": "with open(context_file, 'r') as file_handle:"
    
]
``` something
"""

    with pytest.raises(ValueError) as exc_info:
        extract_mutant_dict_list(input_result)
    assert str(exc_info.value) == "No JSON list found in the input string."

def test_extract_mutant_list_special_characters():
    input_result = """something ```json
[
    {
        "id": 1,
        "line": 16,
        "precode": "    return { 'key': 'value' }",
        "filepath": "project_generator.py",
        "aftercode": "    return { 'key': 'modified_value' }"
    }
]
``` something
"""

    expected_result = [
        {
            'after_code': "    return { 'key': 'modified_value' }",
            'pre_code': "    return { 'key': 'value' }"
        }
    ]

    actual_result = extract_mutant_dict_list(input_result)
    assert actual_result == expected_result
