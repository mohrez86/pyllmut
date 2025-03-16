from pyllmut.mutant_lib import mutant_manager
from pyllmut.mutant_lib.mutant_classifier import MutantClassifier
from pyllmut.mutant_lib.mutant_type import MutantType
from tests import utils


def test_classifier_1():
    module_path = utils.get_cookiecutter_1_generate_py_path()
    module_content = module_path.read_text()
    line_number = 20
    pre_code_model = "from cookiecutter.utils import make_sure_path_exists, rmtree, work_in"
    after_code_model = "from cookiecutter.utils import make_sure_path_exists, remove, work_in"

    mutant_dict = {
        "pre_code": pre_code_model,
        "after_code": after_code_model
    }

    mutant = mutant_manager.get_mutant(
        prompt_content="Dummy prompt",
        response_content="Dummy response",
        sent_token_count=-1,
        received_token_count=-1,
        module_content=module_content,
        line_number=line_number,
        mutant_dict=mutant_dict
    )

    assert mutant.get_mutant_type() == MutantType.UNKNOWN
    mutant_manager.classify_mutant_list([mutant])
    assert mutant.get_mutant_type() == MutantType.WRONG_REPORT


def test_classifier_2():
    module_path = utils.get_cookiecutter_1_generate_py_path()
    module_content = module_path.read_text()
    line_number = 175
    pre_code_model = "rd.readline()  # Read the first line to load 'newlines' value"
    after_code_model = "rd.readlines()  # Read all lines to load 'newlines' value"

    mutant_dict = {
        "pre_code": pre_code_model,
        "after_code": after_code_model
    }

    mutant = mutant_manager.get_mutant(
        prompt_content="Dummy prompt",
        response_content="Dummy response",
        sent_token_count=-1,
        received_token_count=-1,
        module_content=module_content,
        line_number=line_number,
        mutant_dict=mutant_dict
    )

    assert mutant.get_mutant_type() == MutantType.UNKNOWN
    mutant_manager.classify_mutant_list([mutant])
    assert mutant.get_mutant_type() == MutantType.VALID


def test__code_line_string_equality():
    code_line_1 = "    c = 'abc # xyz'"
    code_line_2 = '    c = "abc # xyz"'
    assert MutantClassifier._code_line_string_equality(code_line_1, code_line_2)
