#!/bin/bash

# Start nginx
nginx

# Start Django application
cd /app/backend
python manage.py migrate
python manage.py runserver 0.0.0.0:8001