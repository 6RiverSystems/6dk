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


pipenv run gunicorn --bind unix:/app/6dk.sock -m 777 wsgi --workers=2 &

nginx -g 'daemon off;'

