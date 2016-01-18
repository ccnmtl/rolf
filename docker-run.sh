#!/bin/bash

cd /app/
/ve/bin/python manage.py migrate --noinput --settings=rolf.settings_docker
/ve/bin/python manage.py collectstatic --noinput --settings=rolf.settings_docker
/ve/bin/python manage.py compress --settings=rolf.settings_docker
exec /ve/bin/gunicorn --env \
  DJANGO_SETTINGS_MODULE=rolf.settings_docker \
  rolf.wsgi:application -b 0.0.0.0:8000 -w 3 \
	-t 600 \
  --access-logfile=- --error-logfile=-
