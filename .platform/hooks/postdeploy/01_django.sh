#!/bin/bash

source /var/app/venv/*/bin/activate && {

pip install django-multiselectfield
python manage.py collectstatic --noinput;
python manage.py showmigrations;
python manage.py migrate --noinput;
DJANGO_SUPERUSER_PASSWORD='12345678'
python manage.py createsuperuser --username 'bkpe' --email 'bkpe@masleap.io' --noinput

}