#!/bin/bash

python manage.py collectstatic --noinput -v 0
python manage.py test
python manage.py runserver 0.0.0.0:8000
