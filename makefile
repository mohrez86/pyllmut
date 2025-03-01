.PHONY: dev tests tests_all tests_expensive docs

dev:
	python -m pip install -r requirements.txt
	python -m pip install -r docs/requirements.txt
	python -m pip install -e .

tests:
	python -m pytest tests

tests_all:
	python -m pytest tests -m "expensive or not expensive"

tests_expensive:
	python -m pytest tests -m "expensive"

docs:
	mkdocs serve
