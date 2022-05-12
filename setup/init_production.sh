#!/usr/bin/env bash
set -e

echo Rebuilding and running Docker container
docker-compose -f docker-compose.prod.yaml up -d --build --force-recreate

echo Collecting static files
docker-compose -f docker-compose.prod.yaml exec -T django site/manage.py generate_code_styles site/static/scss default monokai
docker-compose -f docker-compose.prod.yaml exec -T django site/manage.py compilescss
docker-compose -f docker-compose.prod.yaml exec -T django site/manage.py collectstatic --no-input

# This isn't actually needed in practice, but it's good practice and it can't hurt
echo Installing and building watson
docker-compose -f docker-compose.prod.yaml exec -T django ./site/manage.py installwatson
docker-compose -f docker-compose.prod.yaml exec -T django ./site/manage.py buildwatson

echo Migrating database
docker-compose -f docker-compose.prod.yaml exec -T django site/manage.py migrate

echo Creating development data
docker-compose -f docker-compose.prod.yaml exec -T django site/manage.py create_dev_data

echo Shutting down Docker container
docker-compose -f docker-compose.prod.yaml down
