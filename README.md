# Taktlausveven

Studentorchesteret Dei Taktlause's new website.

## Development

### Installation

Requires [Docker](https://docs.docker.com/get-docker/) and [docker-compose](https://docs.docker.com/compose/install/).

- Clone the repository.
- Clone submodules with `git submodule update --init --recursive`
- Build containers and initialize the database with `sh scripts/reset.sh`.

A superuser with the username "leiar" and the password "password" is created automatically when initializing the database. Users "aspirant", "medlem", and "pensjonist" are also created, with the password "password".

### Running

- Run the project with `sh scripts/up.sh`. The site is accessible at [localhost:8000](http://localhost:8000/). Stop it with `Ctrl+C`.

### Building

- When you make changes to any dependencies for [`Dockerfile`](./Dockerfile), rebuild containers with `docker-compose build`

### Running other commands

- Run a single Django command in the Docker container with `sh scripts/run.sh site/manage.py <command>`
- Run a single shell command in the Docker container with `sh scripts/run.sh <command>`
- Run Docker container as interactive shell with `sh scripts/run.sh`

### Cleanup

- Stop and remove Docker containers with `docker-compose down`
- Remove database volume with `docker volume rm taktlausveven_db_dev`

### Code Quality

The project uses [Django's test framework](https://docs.djangoproject.com/en/4.0/topics/testing/) for tests, [autoflake](https://github.com/myint/autoflake) to remove unsused imports, [isort](https://pycqa.github.io/isort/index.html) to sort imports, [Black](https://black.readthedocs.io/en/stable/) for formatting, and [flake8](https://flake8.pycqa.org/en/latest/) for linting.

- Run tests with `sh scripts/test.sh`
- Remove unused imports, sort imports, format all files and lint with `sh scripts/lint.sh`

### Overview of handy shell scripts

- `sh scripts/up.sh`: Run dev server.
- `sh scripts/down.sh`: Stop and remove all running containers.
- `sh scripts/reset.sh`: Remove database volume, delete media files and initialize new dev data.
- `sh scripts/run.sh`: Enter docker container as bash shell.
- `sh scripts/run.sh <command>`: Run `<command>` in docker docker container bash shell.
- `sh scripts/lint.sh`: Run formatter and linter.
- `sh scripts/test.sh`: Run all tests.
- `sh scripts/test.sh <app_name>`: Run tests for a single app.
- `sh scripts/verify.sh`: Run formatter, linter and tests.
- `sh scripts/startapp.sh <app_name>`: Initialize a new django app with the name "app_name".
- `sh scripts/migrate.sh`: Make migrations and migrate.

## Running locally in production mode

You can run in production mode locally, by following these steps:

1. Create an environment file `deployment/.prod.env` with the following content:

```env
DEBUG=0
PRODUCTION=1
ALLOWED_HOSTS=.localhost 127.0.0.1 [::1]
CSRF_TRUSTED_ORIGINS=https://localhost

CERTBOT_EMAIL=www@taktlaus.no
USE_LOCAL_CA=1

POSTGRES_DB=taktlaus_db
POSTGRES_USER=taktlaus
POSTGRES_PASSWORD=taktlaus
```

2. `sh scripts/reset_production.sh`

That was all for the first-time setup. You can hereby start and build the production server with `docker-compose -f docker-compose.prod.yaml up --build --force-recreate`. If you add migrations or change other dependencies of the commands in [`scripts/reset_production.sh`](scripts/reset_production.sh), you have to rerun the script.

The site is now served at `localhost`, at the browser's default ports (80/443), instead of usual 8000. Loading the page gives you a security warning because the browser doesn't recognize the custom HTTPS certificate, this can safely be ignored. Another solution is to import the certificate into your browser, as explained [here](https://github.com/JonasAlfredsson/docker-nginx-certbot/blob/master/docs/advanced_usage.md#local-ca).
