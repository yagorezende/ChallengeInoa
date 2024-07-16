.PHONY: run build
	
run:
	python3 manage.py runserver 8000

build:
	docker build . -t tag

run-docker:
	docker run -p 8000:8000 tag
