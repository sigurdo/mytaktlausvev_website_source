#!/usr/bin/env bash
set -e

docker-compose build

docker-compose run web ./manage.py migrate
docker-compose run web ./manage.py createsuperuser --username=taktlaus --email=www@taktlaus.no

docker-compose down
