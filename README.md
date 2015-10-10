#Cumets Server Backend

Api de la celebre application qui te permet de t'adonner a des plaisirs solitaires sans etre caught.
Keep on crossing in a free world

## Installation

Il faut un postgresql avec postgis d’installé (apt-get install postgresql-9.4-postgis-2.1).
Il faut ensuite créer un utilisateur postgres nommé cumets avec mot de passe cumets et créer l’extension postgis:
```
CREATE role cumets PASSWORD 'cumets' LOGIN;
CREATE EXTENSION postgis;
```

Pour créer la base de données, il faut lancer
```
python app.py create
```
