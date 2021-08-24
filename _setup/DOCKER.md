# What to install
The docker setup needs docker and docker-compose.

# Initial setup
The initial test database, with a superuser included, can be built with the "database_init.sh" script.

# Run the server
To run the server, run "docker-compose build" and "docker-compose up -d", shut down with "docker-compose down".
The site is accessible at localhost:8080, the database is permanently stored at "/scratch/taktlaus_db" between runns.
To clear the database, simply remove it and rerun "database_init.sh".
