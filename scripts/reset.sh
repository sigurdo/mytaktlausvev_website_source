#!/bin/sh
set -e               # Exit on error
cd $(dirname $0)/../ # Set working directory to project root

echo Stopping Docker container and dropping database
docker-compose down -v --remove-orphans

echo Deleting media files
rm -rf site/media/
mkdir site/media/

echo Rebuilding and running Docker container
docker-compose build
docker-compose up -d

echo Generating code styles
docker-compose exec -T django ./site/manage.py generate_code_styles site/static/scss default monokai

echo Migrating database
docker-compose exec -T django ./site/manage.py migrate

echo Creating development data
docker-compose exec -T django ./site/manage.py create_dev_data

echo Installing and building watson
docker-compose exec -T django ./site/manage.py installwatson
docker-compose exec -T django ./site/manage.py buildwatson

echo Stopping Docker container
docker-compose down
