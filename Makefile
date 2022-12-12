SHELL := /bin/bash

env-setup:
	rm -rf venv
	python3 -m venv venv; \
	source venv/bin/activate; \
	pip install --upgrade pip; \
	pip install -r requirements.txt

pre-commit-mac:
	brew install pre-commit
	pre-commit install
	pre-commit run --all-files

setup-docker:
	docker-compose down
	export ENV=docker; \
	export DOCKER_DEFAULT_PLATFORM=linux/amd64; \
	docker-compose up

pre-fill-db:
	source venv/bin/activate; \
	python manage.py makemigrations; \
	python manage.py migrate; \
	python manage.py shell < setup_db/script.py

setup-docker-clean:
	docker-compose down
	docker volume prune

django:
	source venv/bin/activate; \
	python manage.py makemigrations; \
	python manage.py migrate; \
	python manage.py runserver 0.0.0.0:8000

docker-image:
	export ENV=docker; \
	docker-compose build

run-tests:
	pytest
