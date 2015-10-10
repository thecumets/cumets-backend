from flask import Blueprint, request, abort, jsonify
from database import db
from models import User

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
    db.session.add(user)
    db.session.commit()

    return jsonify({
        "creation": "success"
    })


@bp.route("/login")
def login():
    pass
