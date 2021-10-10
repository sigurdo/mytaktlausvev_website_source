# Docker

## What to install

The Docker setup needs [Docker](https://docs.docker.com/get-docker/) and [docker-compose](https://docs.docker.com/compose/install/).

## Initial setup

The initial dev database, with a superuser included, can be built with the [`init.sh`](./init.sh) script.
The superuser will have the username "leiar" and the password "password".

It sometimes happens that the setup script fails, warning that the database is not connected. This is a bug in the Docker setup that should be fixed, but can be easily circumvented by rerunning the script.
The bug is caused by a race condition between the two Docker images.

## Run the server

To run the server, build the project with `docker-compose build` and run with `docker-compose up`. Stop and remove Docker containers with `docker-compose down`.

The site is accessible at [localhost:8000](localhost:8000), and the database is permanently stored at "~/taktlaus_db" between runs.
To clear the database, simply remove it and rerun [`init.sh`](./init.sh).

Note that `docker-compose up` can be run with the `-d` option (detach) to run the server in the background.
Accessing the live logs is still possible by entering the the live docker containers, though this is a bit more complicated and depends on the exact use case.

## Extra build steps for sheetmusic

Docker build steps required for the sheetmusic uploader are skipped by default. To use the sheetmusic uploader you must build your docker container with `--build-arg SHEETMUSIC=yes`, so

```
docker-compose build --build-arg SHEETMUSIC=yes
```
