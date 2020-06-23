POSTGRES_DB=personal_finance

start:
	python manage.py runserver 127.0.0.1:8082

migrate:
	python manage.py makemigrations core
	python manage.py migrate

format:
	black .

lint: typecheck
	flake8
	isort -c -rc src/ tests/

isort:
	isort -rc src/ tests/

shell:
	python3 manage.py shell_plus

test-dev:
	pytest -f -vv -x tests/

typecheck:
	python -m mypy --config-file setup.cfg --package src

recreate-db:
	rm -rf ./src/**/migrations
	dropdb ${POSTGRES_DB}
	createdb ${POSTGRES_DB}

shell:
	python manage.py shell
