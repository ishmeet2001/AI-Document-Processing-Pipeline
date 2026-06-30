PYTHON ?= python
PACKAGE_ROOT := $(CURDIR)/src/unstructured-data-pipeline
export PYTHONPATH := $(PACKAGE_ROOT)

.PHONY: install test lint format clean

install:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -e .

test:
	$(PYTHON) -m pytest

lint:
	$(PYTHON) -m pip install -U ruff
	$(PYTHON) -m ruff check src tests

format:
	$(PYTHON) -m ruff format src tests

clean:
	rm -rf .pytest_cache .ruff_cache **/__pycache__ *.sqlite
