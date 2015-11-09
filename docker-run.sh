#!/bin/bash

cd /var/www/rolf/rolf/
python manage.py migrate --noinput --settings=rolf.settings_docker
python manage.py collectstatic --noinput --settings=rolf.settings_docker
python manage.py compress --settings=rolf.settings_docker
exec gunicorn --env \
  DJANGO_SETTINGS_MODULE=rolf.settings_docker \
  rolf.wsgi:application -b 0.0.0.0:8000 -w 3 \
  --access-logfile=- --error-logfile=-
