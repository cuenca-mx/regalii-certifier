SHELL := bash
PATH := ./venv/bin:${PATH}
PYTHON=python3.6


default: install

venv:
		$(PYTHON) -m venv venv
		source venv/bin/activate
		pip install --quiet --upgrade pip

clean:
		rm -rf venv/

install: venv
		pip install --quiet --upgrade -r requirements.txt

install-dev: install
		pip install --quiet --upgrade -r requirements-dev.txt

lint:
		pycodestyle regalii_certifier tests

certifications:
		pytest -v

mexican-certifications:
		pytest -v tests/test_mexican_suite.py