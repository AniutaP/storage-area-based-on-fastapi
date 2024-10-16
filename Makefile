install:
	poetry install

dev:
	poetry run uvicorn storage_area:app --reload

PORT ?= 8000
start:
	poetry run uvicorn 0.0.0.0:$(PORT) storage_area:app

lint:
	poetry run flake8 storage_area

build:
	poetry build

test:
	poetry run pytest

test-coverage:
	poetry run pytest --cov=storage_area --cov-report xml

check: test lint

package-install:
	python3 -m pip install dist/*.whl

package-reinstall:
	python3 -m pip install dist/*.whl --force-reinstall

.PHONY: install dev start lint build test test-coverage check package-install package-reinstall