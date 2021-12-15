#!/usr/bin/env bash
set -e

echo Runing deployment script on server
cd veven/taktlausveven

echo Pulling updates
git pull
git submodule update --init --recursive

echo Rebuilding Docker container
docker-compose -f docker-compose.prod.yaml up -d --build --force-recreate

echo Migrating database
docker-compose -f docker-compose.prod.yaml exec -T django site/manage.py migrate

echo Collecting static files
docker-compose -f docker-compose.prod.yaml exec -T django site/manage.py generate_code_styles site/static/scss default monokai
docker-compose -f docker-compose.prod.yaml exec -T django site/manage.py compilescss
docker-compose -f docker-compose.prod.yaml exec -T django site/manage.py collectstatic --no-input
