#!/bin/sh
set -e               # Exit on error
cd $(dirname $0)/../ # Set working directory to project root

docker-compose run --rm django autoflake --in-place --remove-all-unused-imports -r site/
docker-compose run --rm django isort .
docker-compose run --rm django black .
docker-compose run --rm django flake8
