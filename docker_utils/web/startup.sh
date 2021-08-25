#!/bin/bash

python manage.py migrate
python manage.py collectstatic --no-input
gunicorn --env DJANGO_SETTINGS_MODULE=votepredictbackend.settings \
  votepredictbackend.wsgi --bind 0.0.0.0:8000 "$RELOAD"
