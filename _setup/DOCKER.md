# What to install
The docker setup needs docker and docker-compose.

# Initial setup
The initial test database, with a superuser included, can be built with the "database_init.sh" script.
The superuser will have the username "taktlaus" and a password set by the user when running the setup script.

It sometimes happens that the setup script fails, warning that the database is not connected. This is a bug in the docker setup that should be fixed, but can be easily circumvented by rerunning the script.
The bug is caused by a race condition between the two docker images.

# Run the server
To run the server, run "docker-compose build" and "docker-compose up -d", shut down with "docker-compose down".
The site is accessible at localhost:8080, the database is permanently stored at "~/taktlaus_db" between runns.
To clear the database, simply remove it and rerun "database_init.sh".

Note that "docker-compose up" can be run without the -d option (detatch) to get the live log from all the containers in the terminal.
It is also possible to access the live loggs by entering the live docker containers, though this is a bit more complicated and depends on the exact use case.
