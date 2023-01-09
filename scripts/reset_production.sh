#!/bin/sh
set -e               # Exit on error
cd $(dirname $0)/../ # Set working directory to project root

echo Stopping Docker container and dropping database
docker-compose -f docker-compose.prod.yaml down -v --remove-orphans

echo Rebuilding and running Docker container
docker-compose -f docker-compose.prod.yaml build
docker-compose -f docker-compose.prod.yaml run --rm django python site/manage.py migrate

echo Creating development data
docker-compose -f docker-compose.prod.yaml run --rm django site/manage.py create_dev_data

echo Stopping Docker container
docker-compose -f docker-compose.prod.yaml down
