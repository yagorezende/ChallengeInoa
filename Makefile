.PHONY: run build run-docker create-key create-user migration
	
run:
	python3 manage.py runserver 8000

build:
	docker build . -t tag

run-docker:
	docker run -p 8000:8000 tag

create-key:
	@echo `python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`

create-user:
	python3 manage.py createsuperuser

migration:
	python3 manage.py makemigrations && python3 manage.py migrate