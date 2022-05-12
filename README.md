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
- `sh test.sh`: Run all tests.
- `sh test.sh <app_name>`: Run tests for a single app.
- `sh verify.sh`: Run formatter, linter and tests.

## Running locally in production mode

You can run in production mode locally, by following these steps:

1. Create an environment file `deployment/.prod.env` with the following content:

```env
DEBUG=0
ALLOWED_HOSTS=.localhost 127.0.0.1 [::1]
CSRF_TRUSTED_ORIGINS=https://localhost

CERTBOT_EMAIL=www@taktlaus.no
USE_LOCAL_CA=1
```

2. Add `localhost` to the `server_name` properties in [`nginx.conf`](deployment/nginx.conf).
3. `docker-compose -f docker-compose.prod.yaml up -d --build --force-recreate`
4. `docker-compose -f docker-compose.prod.yaml exec -T django site/manage.py migrate`
5. `docker-compose -f docker-compose.prod.yaml exec -T django site/manage.py generate_code_styles site/static/scss default monokai`
6. `docker-compose -f docker-compose.prod.yaml exec -T django site/manage.py compilescss`
7. `docker-compose -f docker-compose.prod.yaml exec -T django site/manage.py collectstatic --no-input`
8. `docker-compose -f docker-compose.prod.yaml exec -T django site/manage.py create_dev_data`
9.  You can now load the page, but you will be met by a security warning, because the https certificate is not valid. You can either add the certificate manually as explained [here](https://github.com/JonasAlfredsson/docker-nginx-certbot/blob/master/docs/advanced_usage.md#local-ca), or you can press "Advanced options" and "Accept risk", and it will work totally fine.
10. `docker-compose -f docker-compose.prod.yaml down`

That was all for the first-time setup. You can hereby start and build the production server with `docker-compose -f docker-compose.prod.yaml up --build --force-recreate`. If you add migrations or change other dependencies for the above commands, you have to re-run the respective commands as well. Remember repeating point 3 and 10 before and after.
