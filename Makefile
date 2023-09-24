.PHONY: build
build:
	python -m pipenv install --dev -e .
	sphinx-build -b html docs/source/ docs/build/html
	python -m build
	twine check dist/*

.PHONY: buildt
buildt:
	python -m pipenv install --dev -e .
	rm tests/data/*
	python tests/build_data.py

.PHONY: clean
clean:
	rm -rf docs/build/html
	rm -rf dist
	rm -rf src/imggen.egg-info
	rm -rf tests/__pycache__
	rm -rf tests/*.pyc
	rm -rf src/imggen/__pycache__
	rm -rf src/imggen/*.pyc
	rm -rf src/imggen/pattern/__pycache__
	rm -f *.log
	rm -f *.json
	python -m pipenv uninstall imggen

.PHONY: docs
docs:
	rm -rf docs/build/html
	sphinx-build -b html docs/source/ docs/build/html

.PHONY: pre
pre:
	python -m pipenv install --dev -e .
	python precommit.py
	git status

.PHONY: test
test:
	# python -m pipenv install --dev -e .
	python -m pytest --capture=fd


.PHONY: testv
testv:
	python -m pipenv install --dev -e .
	python -m pytest -vv  --capture=fd
