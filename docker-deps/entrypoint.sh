#!/bin/bash

pipenv run gunicorn --bind unix:/app/6dk.sock -m 007 wsgi --workers=2 &

nginx -g 'daemon off;'

