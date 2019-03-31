# This Makefile requires the following commands to be available:
# * virtualenv
# * python

DEPS:=requirements/requirements-base.txt
VIRTUALENV=$(shell which virtualenv)
PIP:="venv/bin/pip"
CMD_FROM_VENV:=". venv/bin/activate; which"
PYTHON=$(shell "$(CMD_FROM_VENV)" "python3")

.PHONY: venv deploy/qa requirements pyclean clean pipclean killmanage serve shell tests tox test pytests pytest lint isort setup.py publish

venv:
	$(VIRTUALENV) -p $(shell which python3) venv
	. venv/bin/activate
	$(PIP) install -U "pip>=19.0" -q
	$(PIP) install -U -r $(DEPS)

_make_venv_if_empty:
	@[ -e ./venv/bin/python ] || make venv

run/%:
	$(PYTHON) dedupe.py $*


## Utilities for the venv currently active.

_ensure_active_env:
ifndef VIRTUAL_ENV
	@echo 'Error: no virtual environment active'
	@exit 1
endif

requirements: _ensure_active_env
	pip install -U "pip>=19.0" -q
	pip install -U -r $(DEPS)


## Generic utilities.

pyclean:
	find . -name *.pyc -delete
	rm -rf *.egg-info build
	rm -rf coverage.xml .coverage
	rm -rf .pytest_cache
	rm -rf __pycache__

clean: pyclean
	rm -rf venv
	rm -rf .tox
	rm -rf dist

pipclean:
	rm -rf ~/Library/Caches/pip
	rm -rf ~/.cache/pip



