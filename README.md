#Cumets Server Backend

Api de la celebre application qui te permet de t'adonner a des plaisirs solitaires sans etre caught.
Keep on crossing in a free world

## Installation

Pour créer la base de données, il faut lancer
```
python app.py create
```

## Endpoints

### Users

#### POST /users/login

Action:
Loggue l’utilisateur identifié par son facebook_id

Payload:
```
facebook_id
```

#### GET /users/logout

Action:
Déloggue l’utilisateur identifié

Pas de payload.
 

#### GET /users/relate_to/<user_id>

Action:
L’utilisateur loggué sera prévenu lorsque l’utilisateur identifié par user_id s’approche de lui

Pas de payload.


#### POST /users/create

Action:
Crée un nouvel utilisateur

Payload: 

```
token_id
facebook_id
name
```

### Activity

#### GET /activity/start

Action:
L’utilisateur commence une activité, ses personnes à surveiller sont notifiées.

Pas de payload.

#### GET /activity/update

Action:
L’utilisateur reçoit le facebook_id et la distance la personne la plus proche.

Pas de payload.
 

#### GET /activity/disrupt

Action:
L’utilisateur arrête son activité parce que quelqu’un est trop proche.

Pas de payload 


#### GET /activity/stop

Action:
L’utilisateur arrête son activité car il a fini.

Pas de payload.
