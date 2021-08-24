# What to install
The docker setup needs docker and docker-compose.

# Initial setup
The test database is built with "docker-compose run web python manage.py migrate", remember to run "docker-compose down" afterwards.
In the same way, migrations can be made with "docker-compose run web python manage.py makemigrations".

# Run the server
To run the server, run "docker-compose build" and "docker-compose up -d", shut down with "docker-compose down".
The site is accessible at localhost:8080, the database is not permanent.