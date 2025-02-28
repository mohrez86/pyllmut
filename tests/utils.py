import ast
import json
from pathlib import Path


def get_cookiecutter_1_generate_py():
    module_path = Path(__file__).parent / "data" / "cookiecutter_1_generate.py.data"
    module_content = module_path.read_text()
    module_ast = ast.parse(module_content)
    return module_ast, module_content

def get_cookiecutter_1_generate_py_path():
    module_path = Path(__file__).parent / "data" / "cookiecutter_1_generate.py.data"
    return module_path

def get_cookiecutter_1_generate_context_dict():
    context_file_path = Path(__file__).parent / "data" / "cookiecutter_1_generate.py_context.json"
    with context_file_path.open("r") as file:
        context_dict = json.load(file)
    return context_dict

def get_test_data_path(module_name):
    module_path = Path(__file__).parent / "data" / module_name
    return module_path
