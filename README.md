#Cumets Server Backend

Api de la celebre application qui te permet de t'adonner a des plaisirs solitaires sans etre caught.
Keep on crossing in a free world

## Installation

Pour créer la base de données, il faut lancer
```
python app.py create
```

## Workflow

Quand l’utilisateur veut commencer une activité, il fait une requête GET sur /activity/create.

Les applis des personnes à surveiller sont notifiées via un message GCM {"logging": "start"}.
Si leur GPS est éteint, leur appli envoie une requête PUT sur /users/location avec latitude=null et longitude=null.
Si leur GPS est allumé, ils envoient régulièrement une requête PUT sur /users/location avec leur latitude et longitude.

L’utilisateur en cours d’activité peut envoyer une requête GET sur /activity/update.
Il reçoit :
 * l’ID et la distance de la personne la plus proche, 
 * la liste des personnes n’ayant pas updaté leur position depuis plus de 5 minutes,
 * la liste des personnes avec GPS désactivé.

Si l’utilisateur arrête l’activité parce qu’une personne est trop proche, il envoie un GET sur /activity/stop.
Les personnes surveillées reçoivent un message GCM {"logging": "stop"}.

## Endpoints

### Users

#### GET /users/token

Action:
Retourne un token valable 1 an.

Pas de payload.


#### PUT /users/location

Action:
Met à jour la position de l’utilisater loggué.

Payload: 

```
latitude
longitude
```
 

#### PUT /users/monitor/{facebook_id}

Action:
L’utilisateur loggué sera prévenu lorsque l’utilisateur identifié par facebook_id s’approche de lui

Pas de payload.

#### DELETE /users/monitor/{facebook_id}

Action:
L’utilisateur loggué ne sera plus prévenu lorsque l’utilisateur identifié par facebook_id s’approche de lui

Pas de payload.


#### POST /users/create

Action:
Crée un nouvel utilisateur

Payload: 

```
token_id
facebook_id
name
gcm
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
