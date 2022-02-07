docker-compose down
docker volume rm taktlausveven_db_dev
rm -rf site/media/
mkdir site/media/
sh setup/init.sh
