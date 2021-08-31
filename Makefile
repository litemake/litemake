ifeq ($(OS), Windows_NT)
	PY := py
else
	PY := python3
endif

install:
	$(PY) -m pip install -e .

test:
	$(PY) -m pytest --cov nanomake/
