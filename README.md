# Taktlausveven

Studentorchesteret Dei Taktlause's new website.

## Development

### Installation

(For more details, see [setup/DOCKER.md](./setup/DOCKER.md).)

Requires [Docker](https://docs.docker.com/get-docker/) and [docker-compose](https://docs.docker.com/compose/install/).

- Clone the repository
- Clone submodules with `git submodule update --init --recursive`
- Initialize the database with the [`./setup/init.sh`](./setup/init.sh) script
- Build the project with `docker-compose build --build-arg SHEETMUSIC=yes`

A superuser with the username "leiar" and the password "password" is created automatically when initializing the database.

### Running

- Run the project with `docker-compose up`. The site is accessible at [localhost:8000](localhost:8000)
- Run Django commands in the Docker container with `docker-compose run --service-ports web site/manage.py <command>`
- Run Docker container as interactive shell with `docker-compose run --service-ports web bash`
- Stop and remove Docker containers with `docker-compose down`

### Code Quality

The project uses [Black](https://black.readthedocs.io/en/stable/) for formatting and [flake8](https://flake8.pycqa.org/en/latest/) for linting.

- Run tests with `docker-compose run web site/manage.py test site/`
- Format all files with `docker-compose run web black .`
- Lint and verify code style with `docker-compose run web flake8`
