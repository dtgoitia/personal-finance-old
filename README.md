# personal finance

An attempt to make my personal finances easier to manage.

## Install for development

* Requirements:

  - `pipenv` Python package
  - PostgreSQL DB.

```shell
pipenv install --dev
python manage.py migrate
python manage.py createsuperuser
# username: admin
# email: admin@localhost
# password: adminadmin
python manage.py makemigrations core
python manage.py migrate
```

## Usage

...

## Decision log

...
