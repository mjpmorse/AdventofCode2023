PYTHON = '.venv/bin/python'

.PHONY: all

all :
	$(patsubst src/day%, %, $(wildcard src/day*/day*.py))

day%:
	$(PYTHON) src/day$*/day$*.py

test:
	$(PYTHON) -m pytest -vvv .
