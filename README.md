# Taktlausveven

Studentorchesteret Dei Taktlause's new website.

## Development

### Installation

(For more details, see [\_setup/DOCKER.md](./_setup/DOCKER.md).)

Requires [Docker](https://docs.docker.com/get-docker/) and [docker-compose](https://docs.docker.com/compose/install/).

- Clone the repository
- Clone submodules with `git submodule update --init --recursive`
- Initialize the database with the [`database_init.sh`](./_setup/database_init.sh) script
- Build the project with `docker-compose build`
- Run the project with `docker-compose run`

A superuser with the username "leiar" and the password "password" is created automatically when initializing the database.

### Commands

- Run Django commands in the Docker container with `docker-compose run --service-ports web ./site/manage.py <command>`
- Run tests with `docker-compose run --service-ports web ./site/manage.py test site/`
- Run Docker container as interactive shell with `docker-compose run --service-ports web bash`
