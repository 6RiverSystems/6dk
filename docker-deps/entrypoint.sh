#!/bin/bash

pipenv run gunicorn --bind unix:6dk.sock -m 007 wsgi --workers=2 &

nginx -g 'daemon off;'

