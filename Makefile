ifeq ($(OS), Windows_NT)
	PY ?= py
else
	PY ?= python3
endif

.PHONY: dev dev-all ci update-pip install-pre-commit install-compilers test cov

# - - - Installations - - - #

dev: update-pip
	$(PY) -m pip install -e .[dev]

dev-all: update-pip install-pre-commit install-compilers
	$(PY) -m pip install -e .[dev]

ci: update-pip
	$(PY) -m pip install .[dev]

# - - - Helpers - - - #

update-pip:
	$(PY) -m pip install --upgrade pip

install-pre-commit:
	$(PY) -m pip install pre-commit>=2.0
	pre-commit install

install-compilers:
	sudo apt-get update
	sudo apt install clang llvm gcc g++

# - - - Testing - - - #

test:
	$(PY) -m pytest --cov litemake/

cov:
	$(PY) -m pytest --cov litemake/ --cov-report xml --cov-report term
