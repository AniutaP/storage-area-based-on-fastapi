install:
	poetry install

dev:
	poetry run uvicorn src:app --reload

PORT ?= 8000
start:
	poetry run uvicorn 0.0.0.0:$(PORT) src:app

lint:
	poetry run flake8 src

build:
	poetry build

test:
	poetry run pytest

test-coverage:
	poetry run pytest --cov=src --cov-report xml

check: test lint

package-install:
	python3 -m pip install dist/*.whl

package-reinstall:
	python3 -m pip install dist/*.whl --force-reinstall

.PHONY: install dev start lint build test test-coverage check package-install package-reinstall