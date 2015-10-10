from flask import Blueprint, session, abort, jsonify
from database import db
from models import User, Activity
from util import requires_user
from sqlalchemy import and_
import datetime
from haversine import haversine
from gcm_client import gcm


bp = Blueprint("activity", __name__, url_prefix="/activity")
DISTANCE_THRESHOLD = 50


def get_current_activity(user):
    current_activity = Activity.query(and_(Activity.user_id == user.id, Activity.ended_at == None)).first()
    return current_activity

def get_nearest_relation(user):
    min_distance = 10000000
    nearest = None
    user_loc = (user.last_latitude, user.last_longitude)
    for relation in user.relationships:
        loc = (relation.last_latitude, relation.last_longitude)
        distance = haversine(user_loc, loc) / 1000.
        if distance < DISTANCE_THRESHOLD:
            min_distance = distance
            nearest = relation

    return {"user": nearest, "distance": min_distance}


@bp.route("/start")
@requires_user
def start():
    user = User.query.get(session["user_id"])

    current_activity = get_current_activity(user)
    if current_activity is not None:
        abort(412)

    activity = Activity(user.id)

    reg_ids = [relation.gcm for relation in user.relationships if relation.gcm is not None]
    gcm.json_request(registration_ids=reg_ids, data={"logging": "start"})

    db.session.add(activity)
    db.session.commit()
    db.session.flush()
    db.session.refresh(activity)

    return jsonify({
        "start": "success",
        "id": activity.id
    })



@bp.route("/update")
@requires_user
def update():
    user = User.query.get(session["user_id"])

    current_activity = get_current_activity(user)
    if current_activity is None:
        abort(404)

    nearest = get_nearest_relation(user)
    if nearest["distance"] < DISTANCE_THRESHOLD:
        reg_ids = [relation.gcm for relation in user.relationships if relation.gcm is not None]
        gcm.json_request(registration_ids=reg_ids, data={"logging": "stop"})
        current_activity.disrupt(nearest["user"])
        db.session.add(current_activity)
        db.session.commit()
        return jsonify({"activity": "stop"})

    return jsonify({"distance": nearest["distance"]})


@bp.route("/stop")
@requires_user
def stop():
    user = User.query.get(session["user_id"])

    current_activity = get_current_activity(user)
    if current_activity is None:
        abort(404)

    current_activity.ended_at = datetime.datetime.utcnow()
    reg_ids = [relation.gcm for relation in user.relationships if relation.gcm is not None]
    gcm.json_request(registration_ids=reg_ids, data={"logging": "stop"})
    db.session.add(current_activity)
    db.session.commit()

    return jsonify({"stop": "success"})
