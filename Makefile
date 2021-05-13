help:
	@echo "available commands"
	@echo " - dev       : install dev environment"
	@echo " - clean     : clean temporary folders and files"
	@echo " - lint      : checks code style"
	@echo " - test      : runs all unit tests"
	@echo " - coverage  : runs coverage report"
	@echo " - doc       : creates documentation in html"

dev:
	pip install -r requirements-dev.txt
	pre-commit install
	(command -v gitmoji >/dev/null && gitmoji -i) || echo Please install gitmoji-cli

ci:
	python -m pip install --upgrade pip
	pip install flake8 pep8-naming flake8-bugbear flake8-docstrings pytest coverage geopandas

clean:
	rm -rf `find . -type d -name .pytest_cache`
	rm -rf `find . -type d -name __pycache__`
	rm -rf `find . -type d -name .ipynb_checkpoints`
	rm -rf docs/_build
	rm -f .coverage

lint: clean
	flake8

test: clean
	pytest --verbose

coverage: clean
	coverage run -m pytest
	coverage report

