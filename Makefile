.PHONY: run run-docker create-key create-user migration import-b3 start-project
	
run:
	bash runcelery.sh
	python3 manage.py runserver 8000

run-docker:
	docker-compose --env-file .env up --build

create-key:
	@echo `python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`

create-user:
	python3 manage.py createsuperuser

migration:
	python3 manage.py makemigrations && python3 manage.py migrate

import-b3:
	python3 manage.py importb3 --input docs/acoes-listadas-b3.csv

start-project:
	python3 -m venv .venv
	source .venv/bin/activate
	touch db.sqlite3
	cp .env.example .env
	pip install --upgrade pip
	pip install -r requirements.txt
