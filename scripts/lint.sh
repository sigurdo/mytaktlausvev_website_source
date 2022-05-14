# Set workdir to project root
cd "$(dirname "$0")/../"

docker-compose run --rm django autoflake --in-place --remove-all-unused-imports -r site/
docker-compose run --rm django isort .
docker-compose run --rm django black .
docker-compose run --rm django flake8