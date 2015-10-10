from flask import Blueprint, session, abort, jsonify
from database import db
from models import User, Activity
from util import requires_user
from sqlalchemy import and_
import datetime


bp = Blueprint("activity", __name__, url_prefix="/activity")


@bp.route("/start")
@requires_user
def start():
    user = User.query.get(session["user_id"])

    current_activity = Activity.query(and_(Activity.user_id == user.id, Activity.ended_at == None)).first()
    if current_activity is not None:
        abort(412)

    activity = Activity(user.id)
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
    db.session.add(current_activity)
    db.session.commit()

    return jsonify({"stop": "success"})
