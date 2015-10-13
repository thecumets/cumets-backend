from flask import Blueprint, request, abort, jsonify, session, g
from database import db
from models import User
from app import auth

bp = Blueprint("users", __name__, url_prefix="/users")


@bp.route("/create", methods=["POST"])
def create():
    existing = User.query.filter(User.facebook_id == request.form["facebook_id"]).first()
    if existing is not None:
        existing.gcm = request.form["gcm"]
        db.session.commit()
        return jsonify({
            "creation": "success",
            "token": existing.token
        })

    user = User()
    user.name = request.form["name"]
    user.token_id = request.form["token_id"]
    user.facebook_id = request.form["facebook_id"]
    user.gcm = request.form["gcm"]

    user.hash_password(request.form["facebook_id"])

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "creation": "success",
        "token": user.token
    })


@bp.route("/monitor/<string:facebook_id>", methods=["PUT"])
#@auth.login_required
def monitor(facebook_id):
    user = User.query.filter(User.token == request.headers.get("X-Auth-Token")).first()

    if user is None:
        abort(403)

    relation = User.query.filter(User.facebook_id == facebook_id).first()
    if relation is None:
        abort(404)

    if relation in user.relationships:
        return jsonify({"relation": "already in relation"})

    user.relationships.append(relation)
    db.session.add(user)
    db.session.commit()

    return jsonify({"monitor": "success"})


@bp.route("/monitor/<string:facebook_id>", methods=["DELETE"])
#@auth.login_required
def unmonitor(facebook_id):
    user = User.query.filter(User.token == request.headers.get("X-Auth-Token")).first()

    if user is None:
        abort(403)

    relation = User.query.filter(User.facebook_id == facebook_id).first()
    if relation is None:
        abort(404)

    user.relationships.remove(relation)
    db.session.add(user)
    db.session.commit()

    return jsonify({"unmonitor": "success"})


@bp.route("/location", methods=["PUT"])
#@auth.login_required
def update_location():
    user = User.query.filter(User.token == request.headers.get("X-Auth-Token")).first()

    if user is None:
        abort(403)

    if request.form["latitude"] is not None and request.form["longitude"] is not None:
        user.last_latitude = float(request.form["latitude"])
        user.last_longitude = float(request.form["longitude"])
    else:
        user.last_latitude = None
        user.last_longitude = None

    #db.session.add(user)
    db.session.commit()

    return jsonify({"location": "update"})


@bp.route("/token", methods=["GET"])
#@auth.login_required
def token():
    user = User.query.filter(User.token == request.headers.get("X-Auth-Token")).first()

    if user is None:
        abort(403)

    return jsonify({'token': user.generate_auth_token().decode('ascii')})
