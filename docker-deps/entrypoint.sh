#!/bin/bash
cd /app || exit

while true; do
    pipenv run flask db upgrade
    if [[ "$?" == "0" ]]; then
        break
    fi
    echo Upgrade command failed, retrying in 5 secs...
    sleep 5
done

pipenv run gunicorn -k gthread --bind unix:/app/6dk.sock -m 777 wsgi --threads=10 --workers=3 &

nginx -g 'daemon off;'

