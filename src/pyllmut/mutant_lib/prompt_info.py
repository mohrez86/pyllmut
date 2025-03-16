class PromptInfo:
    """A class to store information about a prompt for generating mutants."""

    def __init__(
            self,
            prompt_content: str,
            original_module_content: str,
            line_number: int
    ):
        """
        Initializes the PromptInfo object with the given parameters.

        Args:
            prompt_content (str): The content of the prompt.
            original_module_content (str): The content of the module we plan to generate mutants for.
            line_number (int): The line number in the module where we want to generate mutants.
        """
        self._prompt_content = prompt_content
        self._original_module_content = original_module_content
        self._line_number = line_number

    def get_prompt_content(self) -> str:
        """Returns the content of the prompt."""
        return self._prompt_content

    def get_original_module_content(self) -> str:
        """Returns the content of the module we plan to generate mutants for."""
        return self._original_module_content

    def get_line_number(self) -> int:
        """Returns the line number in the module where we want to generate mutants."""
        return self._line_number
