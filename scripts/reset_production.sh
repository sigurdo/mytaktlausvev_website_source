#!/bin/sh
set -e               # Exit on error
cd $(dirname $0)/../ # Set working directory to project root

echo Stopping Docker container and dropping database
docker-compose -f docker-compose.prod.yaml down -v --remove-orphans

echo Rebuilding and running Docker container
docker-compose -f docker-compose.prod.yaml up -d --build --force-recreate

echo Collecting static files
docker-compose -f docker-compose.prod.yaml exec -T django site/manage.py generate_code_styles site/static/scss default monokai
docker-compose -f docker-compose.prod.yaml exec -T django site/manage.py compilescss
docker-compose -f docker-compose.prod.yaml exec -T django site/manage.py collectstatic --no-input

echo Migrating database
docker-compose -f docker-compose.prod.yaml exec -T django site/manage.py migrate

# This isn't actually needed in practice, but it's good practice and it can't hurt
echo Installing watson
docker-compose -f docker-compose.prod.yaml exec -T django ./site/manage.py installwatson

echo Creating development data
docker-compose -f docker-compose.prod.yaml exec -T django site/manage.py create_dev_data

echo Stopping Docker container
docker-compose -f docker-compose.prod.yaml down
