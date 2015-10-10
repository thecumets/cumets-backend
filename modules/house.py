from flask import Blueprint, request, jsonify, abort
from database import db
from models import House, User


bp = Blueprint("house", __name__, url_prefix="/house")


@bp.route("/create", methods=["POST"])
def create():
    owner = User.query.filter(User.facebook_id == request.form["facebook_id"]).first()
    if owner is None:
        abort(400)

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


@bp.route("/edit")
def edit():
    pass


@bp.route("/delete/<int:house_id>")
def delete(house_id):
    house = House.query.get(house_id)
    if house is None:
        abort(404)

    db.session.delete(house)
    db.session.commit()

    return jsonify({"deletion": "success"})
