#!/bin/sh
cd $WORKDIR
python manage.py collectstatic --noinput

gunicorn rookly.wsgi --timeout 999999 -c gunicorn.conf.py
