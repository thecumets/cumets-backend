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

    current_activity = Activity.query(and_(Activity.user_id == user.id, Activity.ended_at == None)).first()
    if current_activity is not None:
        abort(412)

    activity = Activity(user.id)

    nearest = get_nearest_relation(user)
    if nearest["distance"] < DISTANCE_THRESHOLD:
        activity.disrupt(nearest["user"])
        db.session.add(activity)
        db.session.commit()

        return jsonify({
            "start": "failure",
            "reason": "Someone is close",
            "distance": nearest["distance"]
        })

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


@bp.route("/stop/<int:activity_id>")
@requires_user
def stop(activity_id):
    user = User.query.get(session["user_id"])

    current_activity = Activity.query.get(activity_id)
    if current_activity is None:
        abort(404)

    if current_activity.user != user:
        abort(401)

    current_activity.ended_at = datetime.datetime.utcnow()
    reg_ids = [relation.gcm for relation in user.relationships if relation.gcm is not None]
    gcm.json_request(registration_ids=reg_ids, data={"logging": "stop"})
    db.session.add(current_activity)
    db.session.commit()

    return jsonify({"stop": "success"})
