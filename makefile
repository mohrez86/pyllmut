# Makefile for setting up the development environment, testing, and serving documentation
#
# This Makefile defines targets for:
# - dev: setting up the development environment
# - dev_docs: setting up the documentation environment
# - tests: running all tests except expensive ones
# - tests_all: running all tests, including expensive ones
# - tests_expensive: running only the expensive tests (tests that involve LLM API calls)
# - docs: serving the documentation locally using MkDocs
#
# Usage:
# - To set up the development environment, run: `make dev`
# - To set up the documentation development environment, run: `make dev_docs`
# - To run all tests except expensive ones, run: `make tests`
# - To run all tests, including expensive ones, run: `make tests_all`
# - To run only the expensive tests, run: `make tests_expensive`
# - To serve the documentation locally, run: `make docs`

.PHONY: dev dev_docs tests tests_all tests_expensive docs

# Target to set up the development environment.
# Installs required dependencies from requirements.txt, and installs the current package in editable mode.
dev:
	python -m pip install -r requirements.txt
	python -m pip install -e .

# Target to set up the documentation development environment.
# Installs the required dependencies for documentation from docs/requirements.txt
# and installs the current package in editable mode.
dev_docs:
	python -m pip install -r docs/requirements.txt
	python -m pip install -e .

# Target to run all tests except the expensive ones.
# Uses pytest to execute all tests located in the tests directory, excluding expensive tests.
tests:
	python -m pytest tests

# Target to run all tests, including the expensive ones.
# Uses pytest to execute all tests, including those marked as "expensive".
tests_all:
	python -m pytest tests -m "expensive or not expensive"

# Target to run only the expensive tests.
# Uses pytest to execute only tests marked as "expensive".
# Expensive tests involve connecting to LLM APIs, which may incur costs.
tests_expensive:
	python -m pytest tests -m "expensive"

# Target to serve the documentation locally.
# Starts the MkDocs server for local preview of the documentation.
docs:
	mkdocs serve
