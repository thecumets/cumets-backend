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

Payload :
```
facebook_id
```

#### GET /users/logout

Pas de payload 


#### POST /users/create
Payload : 

```
token_id
facebook_id
name
```

### House

### POST /house/create

Crée une maison dont le propriétaire est l’utilisateur loggué

Payload : 

```
name
latitude
longitude
```

### GET /house/join/<house_id>

L’utilisateur loggué rejoint la maison qui a l’id house_id.

### GET /house/delete

L’utilisateur détruit sa maison, uniquement s’il en est le propriétaire.
