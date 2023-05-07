install:
	pip3 install -r requirements.txt

test:
	pytest

format:
	black myproject

migrate:
	python3 manage.py migrate

createsuperuser:
	python3 manage.py createsuperuser