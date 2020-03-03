Her er en liste over alt som gikk gærent da jeg (Sigurd) satte opp skikkelig database:

# MySQL

1. egg_info. For det første må man installere noe verktøy som kan kommunisere med databasen for deg. Noen alternativer er `sudo apt install python3.6-dev libmysqlclient-dev` eller `pip install mysqlclient`. Jeg tror de gjør det samme, men hvis den ene feiler, prøv den andre i tillegg. Jeg har mest trua på den med pip egt. MEN i windows så funker jo ikke den første uansett, og dessuten er det et problem med akkurat den pakka der, fordi den kommandoen direkte peker til en `.tar.gz`-fil og ikke `.whl`. Det du da må gjøre er å gå til https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient og laste ned den utgaven som passer din versjon av python. Du lagrer den fila i `taktlausveven/site/` og installerer den med `pip install [filnavn]`. TADAAA! Du bør nå ha fått installert mysqlclient.
2. Access denied/Can't connect to database. For det andre hadde jeg en merkelig bug med tilgang fordi når jeg lagde databasebrukeren tillot jeg tilkobling fra any hostname, men jeg burde ha satt kun localhost fordi det førte til at databasen tillot tilkobling fra alle hostnames unntatt localhost. Dette var visstnok på grunn av en allerede eksisterende bruker any_name@localhost, som ikke hadde tilgang. Men egt bør du uansett sette hostname til kun localhost, fordi det er veldig uvanlig om en annen server enn localhost skulle trenge tilgang til databasen.

# Postgres

1. egg_info. Samme problem som for MySQL, man må installere verktøy for å kommunisere med databasen. Man må enten kjøre `sudo apt install python3.6-dev libpq-dev` eller `pip install psycopg2`, eller kanskje helst begge. Men, hmmmm, det er mulig bare den andre trengs... Jeg må teste ut det her litt merker jeg.

Jeg tror det var alt hvertfall...
