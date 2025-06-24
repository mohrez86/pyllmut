# PyLLMut Changelog

## PyLLMut 0.6.0

- Fixed a crashing bug in the `source_lib` package related to finding
  function AST node end lines in Python versions prior to 3.8.

## PyLLMut 0.5.0

- Fix computation of docstring start and end lines for Python 3.7 and add test for `_is_docstring_line`.
- Fix `end_lineno` attribute error on Python versions earlier than 3.8. 
- Relax `openai` dependency.
- Remove `black` dependency and config.
- Updated minimum supported Python version to 3.7.
- Revise development and documentation dependencies.

##  PyLLMut 0.4.0

- Revise the Quick Start page of the documentation.
- Enhance the `MutantGenerator` class to take the model as a parameter.
- Add support for the `GPT-4o` model.
- Refactor some modules.

## PyLLMut 0.3.0

- Update test workflows to support multiple OS and Python versions.
- Revise documentation.

## PyLLMut 0.2.0

- Add convenience imports in the `__init__.py` module to simplify access to key classes.
- Add PyPI installation instructions to the documentation.
- Add a PyPI badge to the documentation and `README.md`.

## PyLLMut 0.1.0

- The first release.
