# Taktlausveven

Studentorchesteret Dei Taktlause's new website.

## Development

### Installation

(For more details, see [setup/DOCKER.md](./setup/DOCKER.md).)

Requires [Docker](https://docs.docker.com/get-docker/) and [docker-compose](https://docs.docker.com/compose/install/).

- Clone the repository.
- Clone submodules, build containers and initialize the database with the [`init.sh`](./setup/init.sh) script.

A superuser with the username "leiar" and the password "password" is created automatically when initializing the database. Users "aspirant", "medlem", and "pensjonist" are also created, with the password "password".

### Running

- Run the project with `docker-compose up`. The site is accessible at [localhost:8000](http://localhost:8000/).

### Building

- When you make changes to any dependencies for [`Dockerfile`](./Dockerfile), rebuild containers with `docker-compose build`.

### Running other commands

- Run a single Django command in the Docker container with `docker-compose run --rm --service-ports django site/manage.py <command>`.
- Run a single shell command in the Docker container with `docker-compose run --rm --service-ports django <command>`.
- Run Docker container as interactive shell with `docker-compose run --rm --service-ports django bash`.

### Cleanup

- Stop and remove Docker containers with `docker-compose down`.
- Remove database volume with `docker volume rm taktlausveven_db_dev`.

### Code Quality

The project uses [djangos test framework](https://docs.djangoproject.com/en/4.0/topics/testing/) for tests, [autoflake](https://github.com/myint/autoflake) to remove unsused imports, [isort](https://pycqa.github.io/isort/index.html) to sort imports, [Black](https://black.readthedocs.io/en/stable/) for formatting, and [flake8](https://flake8.pycqa.org/en/latest/) for linting.

- Run tests with `docker-compose run --rm django site/manage.py test site/`.
- Remove unused imports with `docker-compose run --rm django autoflake --in-place --remove-all-unused-imports -r site/`.
- Sort imports with `docker-compose run --rm django isort .`.
- Format all files with `docker-compose run --rm django black .`.
- Lint and verify code style with `docker-compose run --rm django flake8`.
