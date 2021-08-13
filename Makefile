
.PHONY: init test format docs bump-minor bump-patch package push-package clean

init:
	python3 -m venv venv; \
	. venv/bin/activate; \
	pip install -e .[dev]

test:
	. venv/bin/activate; \
	pytest test

format:
	. venv/bin/activate; \
	autoflake -r --in-place --remove-all-unused-imports --ignore-init-module-imports src test; \
	isort src test; \
	black src test; \
	flake8 src test

docs:
	. venv/bin/activate; \
	sphinx-build -b html docs docs/_html

bump-minor:
	. venv/bin/activate; \
	bumpversion minor

bump-patch:
	. venv/bin/activate; \
	bumpversion patch

package:
	. venv/bin/activate; \
	python setup.py sdist bdist_wheel; \
	twine check dist/*

push-package:
	. venv/bin/activate; \
	twine upload dist/*

clean:
	rm -rf .pytest_cache docs/_html build dist src/dagio.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} \+