# Kjøring og oppsett

## Oppsett av Python
1. Lag et virtual-environment i Python under mappen som heter "site". Dette er muligens valgfritt, men gjør det i alle fall enklere å holde styr på pakkene som siden trenger. Det finnes nok også sannsynligvis innebygd funksjonalitet som gjør dette for deg om du bruker en IDE.

2. Installer pakkene spesifisert i requirements.txt (ved å kjøre `pip install -r requirements.txt`)

## Oppsett av MySQL-server
__Mulig dette steget ikke blir nødvendig om man får egen test-database på en eller annen server i fremtiden__
1. Last ned en MySQL-server-løsning, [for eksempel her.](https://dev.mysql.com/downloads/windows/installer/8.0.html) (eller for tilsvarende operativsystem)
2. Når du starter installasjonen så trenger du egentlig ikke å installere alt. På Windows kan du egentlig klare deg med "Developer Default"-innstillingen, men om du ikke har lyst til å installere masse unødvendige greier kan du velge custom. Under vinduet der du kan velge "products and features" som du vil installere må du ha følgende:
- MySQL Server 8.x.x
- Connector/Python 8.x.x (under MySQL Connectors > Connector/Python)

3. Når man blir bedt om å konfigurere MySQL-serveren kan du egentlig bare bruke standardverdiene. Men under **Accounts and Roles** må du oppgi et root-passord (som kan være hva som helst, må huske det selv), og lage en MySQL-brukerkonto. Denne kan du egentlig kalle hva som helst, og bruke hva som helst som passord, men det skal straks brukes i en annen fil i prosjektet. Denne brukeren burde ha adminrettigheter.
4. Finn ut hvor du installerte MySQL-serveren (på Windows: vanligvis `C:\Program Files\MySQL\MySQL Server 8.0\bin`), og legg de til i PATH. (eller bare sett det opp slik at du kan få tak i `mysql` i et terminalvindu)
5. Skriv `mysql -u root -p` i et terminalvindu, og skriv inn rootpassordet ditt. (du er nå logget inn)
6. Lag en ny database som du kaller `taktlause`. (CREATE DATABASE taktlause;)

7. Lag en ny fil under site/web/ som du kaller settings.cnf. Denne skal ha følgende innhold:
```
[client]
database = taktlause
host = localhost
user = BRUKERNAVNET_DU_VALGTE
password = PASSORDET_DU_VALGTE
default-character-set = utf8
```