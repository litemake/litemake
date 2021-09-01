ifeq ($(OS), Windows_NT)
	PY := py
else
	PY := python3
endif

install:
	$(PY) -m pip install --upgrade pip
	$(PY) -m pip install .

develop:
	$(PY) -m pip install --upgrade pip
	$(PY) -m pip install -e .[dev]

test:
	$(PY) -m pytest --cov nanomake/

cov:
	$(PY) -m pytest --cov nanomake/ --cov-report xml --cov-report term
