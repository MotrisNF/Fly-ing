SHELL := /bin/bash
.SILENT:
ENV_SOURCE=.venv
PYTHON=$(ENV_SOURCE)/bin/python
PIP=$(ENV_SOURCE)/bin/pip
MYPY=mypy --warn-return-any --warn-unused-ignores \
	--ignore-missing-imports \
	--disallow-untyped-defs \
	--check-untyped-defs


env:
	@python3 -m venv $(ENV_SOURCE)

install: env
	@$(PIP) install -r requirements.txt > /dev/null

run: install
	@$(PYTHON) main.py

destroy:
	rm -rf $(ENV_SOURCE)

re-install: destroy install

clean:
	rm -rf .mypy_cache && rm -rf __pycache__

lint: install
	if $(PYTHON) -m flake8 .; then \
		echo "Flake8 without issues"; \
	fi; \
	$(PYTHON) -m $(MYPY) .; \
	true

lint-strict: install
	if $(PYTHON) -m flake8 .; then \
		echo "Flake8 without issues"; \
	fi; \
	$(PYTHON) -m $(MYPY) --strict .; \
	true

.PHONY: env install run destroy re-install lint lint-strict