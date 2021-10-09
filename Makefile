ifeq ($(OS), Windows_NT)
	PY ?= py
else
	PY ?= python3
endif

install:
	$(PY) -m pip install --upgrade pip
	$(PY) -m pip install .

install-compilers:
	sudo apt-get update
	sudo apt install clang llvm gcc g++

develop:
	$(PY) -m pip install --upgrade pip
	$(PY) -m pip install -e .[dev]
	pre-commit install

test:
	$(PY) -m pytest --cov litemake/

cov:
	$(PY) -m pytest --cov litemake/ --cov-report xml --cov-report term


.PHONY: intall install-compilers develop test cov
