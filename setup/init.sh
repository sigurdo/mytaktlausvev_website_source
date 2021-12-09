#!/usr/bin/env bash
set -e

docker-compose build

docker-compose run django ./site/manage.py migrate
docker-compose run django ./site/manage.py create_dev_data
docker-compose run django ./site/manage.py generate_code_styles site/static/scss default monokai

docker-compose down
