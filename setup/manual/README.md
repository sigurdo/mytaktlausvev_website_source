# Kjøring og oppsett

## Oppsett av Python
1. Lag et virtual-environment i Python under mappen som heter "site". Dette er muligens valgfritt, men gjør det i alle fall enklere å holde styr på pakkene som siden trenger. Det finnes nok også sannsynligvis innebygd funksjonalitet som gjør dette for deg om du bruker en IDE.


(venv er bare navnet på mappa inneholder det virtuelle ¿miljøet?)
```
sudo pip3 install virtualenv
virtualenv -p python3 venv
source venv/bin/activate
```

2. Installer pakkene spesifisert i requirements.txt (ved å kjøre `pip install -r requirements.txt`)

## Oppsett av postgresql server
1. last ned postgressql og sånt:

`sudo apt-get update`

`sudo apt-get install python3-pip python3-dev libpq-dev postgresql postgresql-contrib`

eller windows: [postgres.org/download](https://www.postgresql.org/download/windows/)

2. Det ble laget en egen postgres-bruker under installasjonen, logg inn der 

`sudo su - postgres`

og gå inn i databasesesjonen

`psql`

3. lag database og bruker

`CREATE DATABASE taktlaus_db;`

`CREATE USER taktlaus WITH PASSWORD 'taktlaus';`

så endre til utf8 

`ALTER ROLE taktlaus SET client_encoding TO 'utf8';`

`ALTER ROLE taktlaus SET default_transaction_isolation TO 'read committed';`

`ALTER ROLE taktlaus SET timezone TO 'UTC';`

og gi alle rettigheter til brukeren 

`GRANT ALL PRIVILEGES ON DATABASE taktlaus_db TO taktlaus;`

gå ut av brukeren med 

`\q`

`exit`


4. installér requirements.txt hvis du ikke har gjort det (se lenger oppe)

5. endre databaseinstillinger i settings.py

```
. . .

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'taktlaus_db',
        'USER': 'taktlaus',
        'PASSWORD': 'taktlaus',
        'HOST': 'localhost',
        'PORT': '',
    }
}

. . .
```

6. utfør endringene på databasen
```
python manage.py makemigrations
python manage.py migrate
```

7. importer testdata for utvikling

```
python manage.py create_dev_data
```

8. start server

```
python manage.py runserver
```

siden skal nå kjøre på [localhost](http://localhost:8000/)


Alt er skamløst stjålet fra [digitalocean](https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-14-04)


## Sette opp tools for noteopplasteren

For linux: (må kjøres fra root-mappa i repoet)

```
sudo sh setup/sheetmusic.sh
```
