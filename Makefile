##########################################
# Makefile for defining a Management CLI #
##########################################

# Setting up shell and python
SHELL := /bin/bash
PYTHON := python3

# Some constants
VENV_DIR_LINK = venv
VENV_DIR = .api-venv
TEST_VENV_DIR = .testing-venv
SHELL_NAME = bash

.PHONY: help clean clean-venv clean-temp-files venv test-venv install install-dev test pytest cover coverage lint flake8

help:
	@echo "usage: make <command>"
	@echo
	@echo "  clean            [alias] for running \"clean-venv\" and \"clean-temp-files\" sequentially."
	@echo "  clean-venv       to cleanup the virtualenv directories and links."
	@echo "  clean-temp-files to cleanup the project from temporary files."
	@echo "  venv             to create the virtualenv and its symbolic links."
	@echo "  test-venv        to create the virtualenv for installing dev requirements and running tests."
	@echo "  install          to install the app, runs \"venv\" automatically."
	@echo "  install-dev      to install the app in editable mode, runs \"venv\" automatically." 
	@echo "  test             [alias] for running \"install-dev\" and \"pytest\" sequentially."
	@echo "  pytest           to run the entire tests package."
	@echo "  coverage         to generate unit tests coverage."
	@echo "  help             to display this message."
	@echo


clean-venv:
	@echo "####################################################"
	@echo "# Cleaning up the venv                             #"
	@echo "####################################################"
	@rm -rf $(VENV_DIR)
	@rm -rf $(VENV_DIR_LINK)
	@rm -rf $(TEST_VENV_DIR)
	@echo "Done!"	


clean-temp-files:
	@echo "####################################################"
	@echo "# Cleaning up cached and tmp files                 #"
	@echo "####################################################"
	@rm -rf build
	@rm -rf dist
	@rm -rf *.egg-info
	@rm -rf .tox
	@rm -rf htmlcov
	@rm -rf .cache
	@rm -rf .pytest_cache
	@find . -name "*.*,cover" -delete
	@find . -name "*.pyc" -delete
	@find . -name "*.pyo" -delete
	@find . -name "__pycache__" -exec rm -rf {} \; || echo "";
	@echo "Done!"


clean: clean-venv clean-temp-files


log-py-version:
	@echo -n "[INFO] Make is using the Python version: "
	@$(PYTHON) -c 'import sys; v = sys.version_info; print(f"{v.major}.{v.minor}.{v.micro}-{v.releaselevel}");'


venv:
	@echo "####################################################"
	@echo "# Creating the virtual environment                 #"
	@echo "####################################################"
	@echo "===================================================="
	@$(MAKE) -s log-py-version
	@echo "===================================================="
	@test -d $(VENV_DIR) || $(PYTHON) -m venv $(VENV_DIR)
	@test -d $(VENV_DIR_LINK) || ln -s $(VENV_DIR) $(VENV_DIR_LINK)
	@echo "Done!"


test-venv:
	@echo "####################################################"
	@echo "# Creating the >>> TEST <<< virtual environment    #"
	@echo "####################################################"
	@echo "===================================================="
	@$(MAKE) -s log-py-version
	@echo "===================================================="
	@test -d $(TEST_VENV_DIR) || $(PYTHON) -m venv $(TEST_VENV_DIR);
	@echo "Done!"


install: venv
	@echo "####################################################"
	@echo "# Activating venv & solving dependencies           #"
	@echo "####################################################"
	@. $(VENV_DIR)/bin/activate \
		&& pip install -U pip \
		&& pip install -U . \
		&& python -c "import nltk; nltk.download('stopwords')"
	@echo "Done!"


install-dev: test-venv
	@echo "####################################################"
	@echo "# Creating testing venv and installing dev deps    #"
	@echo "####################################################"
	@. $(TEST_VENV_DIR)/bin/activate \
		&& pip install -U pip \
		&& pip install -e . \
		&& pip install -U -r dev-requirements.txt \
		&& python -c "import nltk; nltk.download('stopwords')"
	@echo "Done!"


VERBOSITY=vq
PYTEST_ARGS=
pytest:
	@echo "####################################################"
	@echo "# [TESTING] RUNNING ALL TESTS                      #"
	@echo "####################################################"
	@cp config/test.conf ~/.config/api.conf
	@cp schemas/schema_in.json /tmp/schema_in.json
	@cp schemas/schema_out.json /tmp/schema_out.json
	@test -d $(TEST_VENV_DIR) || { echo "Please run 'make install-dev' first!"; exit 1; }
	@. $(TEST_VENV_DIR)/bin/activate && py.test --cache-clear -$(VERBOSITY) $(PYTEST_ARGS)


VERBOSITY=vq
test: install-dev
	@$(MAKE) -s pytest VERBOSITY=$(VERBOSITY)


VERBOSITY=vq
cover coverage:
	@echo "####################################################"
	@echo "# [TESTING] ANALYSING TEST COVERAGE                #"
	@echo "####################################################"
	@test -d $(TEST_VENV_DIR) || { echo "Please run 'make install-dev' first!"; exit 1; }
	@. $(TEST_VENV_DIR)/bin/activate \
		&& coverage run --source api/ `which py.test` --cache-clear -$(VERBOSITY) tests/; \
		coverage report; \
		coverage html;
	@echo "coverage report done! To see it run something like 'chromium-browser htmlcov/index.html'"


lint flake8:
	@echo "####################################################"
	@echo "# [TESTING] LINTING CODE WITH FLAK8                #"
	@echo "####################################################"
	@test -d $(TEST_VENV_DIR) || { echo "Please run 'make install-dev' first!"; exit 1; }
	@. $(TEST_VENV_DIR)/bin/activate && flake8 api/ tests/
