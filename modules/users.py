from flask import Blueprint, request, abort, jsonify
from database import db
from models import User

bp = Blueprint("users", __name__, url_prefix="/users")


@bp.route("/create", methods=["POST"])
def create():
    token_id = 0
    facebook_id = 0
    try:
        token_id = int(request.form["token_id"])
        facebook_id = int(request.form["facebook_id"])
    except ValueError:
        abort(400)

    existing = User.query.filter(User.token_id == token_id).first()
    if existing is not None:
        abort(409)

    user = User()
    user.name = request.form["name"]
    user.token_id = token_id
    user.facebook_id = facebook_id
    db.session.add(user)
    db.session.commit()

    return jsonify({"creation": "success"})


@bp.route("/login")
def login():
    pass
