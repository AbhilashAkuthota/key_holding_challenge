#!/usr/bin/env bash

python manage.py collectstatic --noinput

python manage.py migrate --no-input

python manage.py shell < setup_db/script.py

python manage.py runserver 0.0.0.0:8000
