# TeamFive/web

Government web service.

Written in Python 3 and Django 1.11.


## Requirements

- Python 3
- Virtualenv (recommended)


## Config

    cd gov/settings/
    cp local.py.template local.py

And then put appropriate `SECRET_KEY` and `DATABASE` values.

If you want to run in debug mode, replace `from .prod import *` by `from .dev import *`.

Later, this part will be automated with `Makefile`.


## Setup

    pip install -r requirements.txt
    python manage.py migrate
    python manage.py createsuperuser


## Run

    python manage.py runserver 0:12345

