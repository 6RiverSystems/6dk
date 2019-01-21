#!/bin/bash

flask db upgrade

pipenv run gunicorn --bind unix:/app/6dk.sock -m 777 wsgi --workers=2 &

nginx -g 'daemon off;'

