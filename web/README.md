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


## Setup

    pip install -r requirements.txt
    python manage.py migrate


## Run

### Run in debug mode

    python manage.py runserver 0:12345

