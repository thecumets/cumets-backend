from flask import Blueprint, request, abort, jsonify, session
from database import db
from models import Subscription

bp = Blueprint("subscription", __name__, url_prefix="/subscription")


@bp.route("/add", methods=["POST"])
def create():
    existing = Subscription.query.filter(Subscription.email == request.form["email"]).first()
    if existing is not None:
        abort(409)

    subscription = Subscription()
    subscription.email = request.form["email"]

    db.session.add(subscription)
    db.session.commit()

    return jsonify({"Subscription": "success"})