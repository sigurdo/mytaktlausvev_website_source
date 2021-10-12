#!/usr/bin/env bash
set -e

echo Runing deployment scripts on server

echo Pulling updates
#TODO: pull the newest from the master branch


echo Restarting services to update web
sudo systemctl restart gunicorn
sudo systemctl restart nginx

