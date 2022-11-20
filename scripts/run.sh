#!/bin/sh
set -e               # Exit on error
cd $(dirname $0)/../ # Set working directory to project root

if [ $# -eq 0 ]; then
    docker-compose run --rm --service-ports django bash
else
    docker-compose run --rm django $@
fi;
