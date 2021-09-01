#!/usr/bin/env bash
set -e

docker-compose build

docker-compose run web ./site/manage.py migrate
docker-compose run web ./site/manage.py create_dev_data

docker-compose down
