#!/bin/sh
set -e               # Exit on error
cd $(dirname $0)/../ # Set working directory to project root

sh scripts/run.sh python site/manage.py makemigrations
sh scripts/run.sh python site/manage.py migrate
