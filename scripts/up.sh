#!/bin/sh
set -e               # Exit on error
cd $(dirname $0)/../ # Set working directory to project root

docker-compose up
