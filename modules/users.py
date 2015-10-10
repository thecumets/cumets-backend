from flask import Blueprint, request, abort, jsonify, session
from database import db
from models import User
from util import requires_user

bp = Blueprint("users", __name__, url_prefix="/users")


@bp.route("/create", methods=["POST"])
def create():
    existing = User.query.filter(User.facebook_id == request.form["facebook_id"]).first()
    if existing is not None:
        abort(409)

    user = User()
    user.name = request.form["name"]
    user.token_id = request.form["token_id"]
    user.facebook_id = request.form["facebook_id"]
    user.gcm = request.form["gcm"]

    db.session.add(user)
    db.session.commit()

    return jsonify({"creation": "success"})


@bp.route("/relate_to/<string:facebook_id>", methods=["GET"])
@requires_user
def relate_to(facebook_id):
    user = User.query.get(session["user_id"])
    relation = User.query.filter(User.facebook_id == facebook_id).first()
    if relation is None:
        abort(404)

    if relation in user.relationships:
        return jsonify({"relation": "already in relation"})

    user.relationships.append(relation)
    db.session.add(user)
    db.session.commit()

    return jsonify({"relation": "success"})


@bp.route("/location", methods=["POST"])
@requires_user
def update_location():
    user = User.query.get(session["user_id"])

    user.last_latitude = float(request.form["latitude"])
    user.last_longitude = float(request.form["longitude"])

    db.session.add(user)
    db.session.commit()

    return jsonify({"location": "update"})


@bp.route("/login", methods=["POST"])
def login():
    user = User.query.filter(User.facebook_id == request.form["facebook_id"]).first()
    if user is None:
        abort(400)

    session["user_id"] = user.id

    return jsonify({"login": "success"})


@bp.route("/logout", methods=["GET"])
@requires_user
def logout():
    session.pop("user_id", None)
    return jsonify({"logout": "success"})
