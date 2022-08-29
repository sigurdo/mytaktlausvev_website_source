#!/bin/sh
set -e               # Exit on error
cd $(dirname $0)/../ # Set working directory to project root

docker-compose run --rm --service-ports --workdir /app/site/ django python manage.py startapp $1
sudo chown -R $USER:$USER site/$1
