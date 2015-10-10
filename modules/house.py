from flask import Blueprint, request, jsonify, abort, session
from database import db
from models import House, User
from util import requires_user


bp = Blueprint("house", __name__, url_prefix="/house")


@bp.route("/create", methods=["POST"])
@requires_user
def create():
    owner = User.query.get(session["user_id"])

    if owner.house is not None:
        abort(412)

    house = House()
    house.name = request.form["name"]
    house.latitude = request.form["latitude"]
    house.longitude = request.form["longitude"]
    house.owner = owner.id

    owner.house = house

    db.session.add(house)
    db.session.add(owner)
    db.session.commit()

    return jsonify({"creation": "success"})


@bp.route("/join/<int:house_id>")
@requires_user
def join(house_id):
    user = User.query.get(session["user_id"])
    house = House.get(house_id)
    if house is None:
        abort(400)

    user.house = house
    db.session.add(user)
    db.session.commit()

    return jsonify({"addition": "success"})


@bp.route("/delete")
@requires_user
def delete():
    user = User.query.get(session["user_id"])
    if user.house is None:
        abort(412)

    house = House.query.get(user.house.id)
    if house is None:
        abort(404)

    if house.owner != user:
        abort(401)

    db.session.delete(house)
    db.session.commit()

    return jsonify({"deletion": "success"})
