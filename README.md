# Taktlausveven

Studentorchesteret Dei Taktlause's new website.

## Development

### Installation

(For more details, see [setup/DOCKER.md](./setup/DOCKER.md).)

Requires [Docker](https://docs.docker.com/get-docker/) and [docker-compose](https://docs.docker.com/compose/install/).

- Clone the repository.
- Clone submodules with `git submodule update --init --recursive`
- Build containers and initialize the database by running the [`init.sh`](./init.sh) script.

A superuser with the username "leiar" and the password "password" is created automatically when initializing the database. Users "aspirant", "medlem", and "pensjonist" are also created, with the password "password".

### Running

- Run the project with `sh up.sh`. The site is accessible at [localhost:8000](http://localhost:8000/). Stop it with `Ctrl+C`.

### Building

- When you make changes to any dependencies for [`Dockerfile`](./Dockerfile), rebuild containers with `docker-compose build`

### Running other commands

- Run a single Django command in the Docker container with `sh run.sh site/manage.py <command>`
- Run a single shell command in the Docker container with `sh run.sh <command>`
- Run Docker container as interactive shell with `sh run.sh`

### Cleanup

- Stop and remove Docker containers with `docker-compose down`
- Remove database volume with `docker volume rm taktlausveven_db_dev`

### Code Quality

The project uses [Django's test framework](https://docs.djangoproject.com/en/4.0/topics/testing/) for tests, [autoflake](https://github.com/myint/autoflake) to remove unsused imports, [isort](https://pycqa.github.io/isort/index.html) to sort imports, [Black](https://black.readthedocs.io/en/stable/) for formatting, and [flake8](https://flake8.pycqa.org/en/latest/) for linting.

- Run tests with `sh test.sh`
- Remove unused imports, sort imports, format all files and lint with `sh lint.sh`

### Overview of handy shell scripts

- `sh up.sh`: Run dev server.
- `sh full_reset.sh`: Remove database volume, delete media files and initialize new dev data.
- `sh run.sh`: Enter docker container as bash shell.
- `sh run.sh <command>`: Run `<command>` in docker docker container bash shell.
- `sh lint.sh`: Run formatter and linter.
- `sh test.sh`: Run tests.
- `sh verify.sh`: Run formatter, linter and tests.
