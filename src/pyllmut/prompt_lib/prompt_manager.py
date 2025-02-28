from pathlib import Path
from string import Template


def _read_template_to_string(template_path: Path) -> str:
    """
    Reads the content of a template file and returns it as a string.

    Args:
        template_path (Path): The path to the template file.

    Returns:
        str: The content of the template file.
    """
    with template_path.open("r") as file:
        script_content = file.read()

    return script_content


def get_prompt(context_code: str, number_of_mutants: int, code_line_to_be_mutated: str) -> str:
    """
    Generates a prompt string using a template file and the provided context.

    Args:
        context_code (str): The context code to be included in the prompt.
        number_of_mutants (int): The number of mutants to be considered.
        code_line_to_be_mutated (str): The specific line of code to be mutated.

    Returns:
        str: The formatted prompt string with substituted values.
    """
    prompt_template_path = Path(__file__).parent / "templates/prompt.template"

    prompt_template_content = _read_template_to_string(prompt_template_path.resolve())
    template = Template(prompt_template_content)
    prompt_str = template.substitute(
        context_code=context_code,
        number_of_mutants=number_of_mutants,
        code_line_to_be_mutated=code_line_to_be_mutated
    )
    return prompt_str
