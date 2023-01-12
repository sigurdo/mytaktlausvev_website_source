#!/bin/sh
set -e               # Exit on error
cd $(dirname $0)/../ # Set working directory to project root

docker-compose -f website_build/docker-compose.prod.yaml up --build --force-recreate
