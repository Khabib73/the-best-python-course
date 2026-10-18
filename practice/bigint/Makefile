.PHONY: install test docker-build docker-test clean

install:
	poetry install

test:
	poetry run pytest

docker-build:
	docker compose build

docker-test:
	docker compose run --rm test

clean:
	rm -rf .pytest_cache dist
	find . -type d -name __pycache__ -prune -exec rm -rf {} +