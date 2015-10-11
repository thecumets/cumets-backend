from app import auth
from flask import Blueprint, session, abort, jsonify
from database import db
from models import User, Activity
from sqlalchemy import and_
from haversine import haversine
from gcm_client import gcm
from datetime import datetime, timedelta


bp = Blueprint("activity", __name__, url_prefix="/activity")
DISTANCE_THRESHOLD = 50


def get_current_activity(user):
    current_activity = Activity.query(and_(Activity.user_id == user.id, Activity.ended_at == None)).first()
    return current_activity


def get_relations_informations(user):
    min_distance = 10000000
    nearest = None
    stale = []
    no_gps = []
    user_loc = (user.last_latitude, user.last_longitude)
    for relation in user.relationships:
        # If too old, we add the relation to the stale list
        time_diff = (datetime.utcnow() - relation.last_updated) / timedelta(minutes=1)
        if time_diff > 5:
            stale.append(relation.facebook_id)
            continue

        # If the GPS is deactivated, we add it to the no-gps list
        loc = (relation.last_latitude, relation.last_longitude)
        if loc[0] is None:
            no_gps.append(relation.facebook_id)
            continue

        # If the GPS is active and up to date, we test if the relation is the nearest.
        distance = haversine(user_loc, loc) / 1000.
        if distance < DISTANCE_THRESHOLD:
            min_distance = distance
            nearest = relation

    return {"user": nearest, "distance": min_distance, "stale": stale, "no_gps": no_gps}


@bp.route("/start", methods=["GET"])
@auth.login_required
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

    return jsonify({"start": "success"})


@bp.route("/update", methods=["GET"])
@auth.login_required
def update():
    user = User.query.get(session["user_id"])

    current_activity = get_current_activity(user)
    if current_activity is None:
        abort(404)

    nearest = get_relations_informations(user)

    return jsonify({
        "distance": nearest["distance"],
        "user": nearest["user"].facebook_id,
        "no_gps": nearest["no_gps"],
        "stale": nearest["stale"],
    })


@bp.route("/disrupt", methods=["GET"])
@auth.login_required
def disrupt():
    user = User.query.get(session["user_id"])

    current_activity = get_current_activity(user)
    if current_activity is None:
        abort(404)

    nearest = get_relations_informations(user)
    reg_ids = [relation.gcm for relation in user.relationships if relation.gcm is not None]
    gcm.json_request(registration_ids=reg_ids, data={"logging": "stop"})
    current_activity.disrupt(nearest["user"])
    db.session.add(current_activity)
    db.session.commit()

    return jsonify({"disrupt": "success"})


@bp.route("/stop", methods=["GET"])
@auth.login_required
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
