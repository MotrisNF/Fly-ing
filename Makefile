SHELL := /bin/bash
ENV_SOURCE=.venv
PYTHON=$(ENV_SOURCE)/bin/python
PIP=$(ENV_SOURCE)/bin/pip


env:
	python3 -m venv $(ENV_SOURCE)

install: env
	$(PIP) install -r requirements.txt

run: install
	$(PYTHON) main.py

destroy:
	rm -rf $(ENV_SOURCE)

.PHONY: env install run destroy