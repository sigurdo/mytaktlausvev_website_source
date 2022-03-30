#!/usr/bin/env bash
set -e

docker-compose down -v

docker-compose build
docker-compose up -d

docker-compose exec -T django ./site/manage.py generate_code_styles site/static/scss default monokai
docker-compose exec -T django ./site/manage.py migrate
docker-compose exec -T django ./site/manage.py create_dev_data

docker-compose exec -T django ./site/manage.py installwatson
docker-compose exec -T django ./site/manage.py buildwatson

docker-compose down
