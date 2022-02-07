if [ $# -eq 0 ]; then
    docker-compose run --rm --service-ports django bash
else
    docker-compose run --rm --service-ports django $@
fi;
