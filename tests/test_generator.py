"""
This module contains tests that are marked as expensive because they contact
an LLM backend model. These tests are excluded from the default test suite run
to save time and money.

Usage:
    To run all tests (both expensive and non-expensive), execute:
        python -m pytest tests -m "expensive or not expensive"

    To run only the expensive tests, execute:
        python -m pytest tests -m "expensive"
"""

from pprint import pprint

import pytest

from pyllmut import ModelType
from pyllmut.generator import MutantGenerator
from pyllmut.mutant_lib.mutant_type import MutantType
from . import utils

@pytest.mark.expensive
def test_simple():
    module_path = utils.get_cookiecutter_1_generate_py_path()
    module_content = module_path.read_text()
    ground_truth_line_list = [339]
    # ground_truth_line_list = [85]
    # ground_truth_line_list = None

    generator = MutantGenerator(module_content, ground_truth_line_list)
    mutation_report = generator.generate()
    print("\n")
    pprint(mutation_report.get_mutant_list())

@pytest.mark.expensive
def test_simple_gpt_4_o():
    module_path = utils.get_cookiecutter_1_generate_py_path()
    module_content = module_path.read_text()
    line_number_list = [85]

    generator = MutantGenerator(
        module_content,
        line_number_list,
        model_type=ModelType.GPT4o
    )

    mutation_report = generator.generate()
    print("\n")
    pprint(mutation_report.get_mutant_list())

@pytest.mark.expensive
def test_timeout():
    module_path = utils.get_cookiecutter_1_generate_py_path()
    module_content = module_path.read_text()
    ground_truth_line_list = [85, 339]

    generator = MutantGenerator(
        module_content,
        ground_truth_line_list,
        mutants_per_line_count=30,
        timeout_seconds_per_line=3
    )

    mutation_report = generator.generate()
    assert len(mutation_report.get_timeout_info_list()) == 2
    assert len(mutation_report.get_mutant_list()) == 0
    assert len(mutation_report.get_bad_response_info_list()) == 0
    assert len([x for x in mutation_report.get_timeout_info_list() if x.get_line_number() == 85]) == 1
    assert len([x for x in mutation_report.get_timeout_info_list() if x.get_line_number() == 339]) == 1

@pytest.mark.expensive
def test_sample1():
    module_path = utils.get_test_data_path("sample1.py")
    module_content = module_path.read_text()
    line_mut_list = [1]
    generator = MutantGenerator(module_content, line_mut_list)
    mutation_report = generator.generate()
    print("\n")
    pprint(mutation_report.get_mutant_list())

@pytest.mark.expensive
def test_token_error():
    module_path = utils.get_cookiecutter_1_generate_py_path()
    module_content = module_path.read_text()

    line_list_to_mutate = [20]

    generator = MutantGenerator(module_content, line_list_to_mutate)
    mutation_report = generator.generate()
    mutant_list = mutation_report.get_mutant_list()
    assert len(mutant_list) == 1
    assert mutant_list[0].get_mutant_type() == MutantType.WRONG_REPORT
