# Docker

## What to install

The Docker setup needs [Docker](https://docs.docker.com/get-docker/) and [docker-compose](https://docs.docker.com/compose/install/).

## Initial setup

The initial dev database, with a superuser included, can be built with the [`init.sh`](./init.sh) script.
The superuser will have the username "leiar" and the password "password". Users "aspirant", "medlem", and "pensjonist" are also created, with the password "password".

## Build and run the server

To run the server, build the project with `docker-compose build` and run with `docker-compose up`. Stop and remove Docker containers with `docker-compose down`.

The site is accessible at [localhost:8000](http://localhost:8000/), and the database is permanently stored in a Docker volume between runs.
To clear the database, simply run `docker volume rm taktlausveven_db_dev` and rerun [`init.sh`](./init.sh).

Note that `docker-compose up` can be run with the `-d` option (detach) to run the server in the background.
Accessing the live logs is still possible by entering the the live docker containers, though this is a bit more complicated and depends on the exact use case.

## Lighter build without sheetmusic

If you know you don't want to use the sheetmusic app and want to save 1.3GB of network traffic and storage space, you can set `--build-arg SHEETMUSIC=no`, so

```
docker-compose build --build-arg SHEETMUSIC=no
```

Note that this will just save you time on your first build, since the operation is cached by docker after the first build and the cache will not be invalidated unless you change any dependenies of operations before the sheetmusic step in [`Dockerfile`](/Dockerfile).
