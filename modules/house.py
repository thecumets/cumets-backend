from flask import Blueprint, request, jsonify, abort
from database import db
from models import House, User


bp = Blueprint("house", __name__, url_prefix="/house")


@bp.route("/create", methods=["POST"])
def create():
    owner = User.query.filter(User.facebook_id == request.form["facebook_id"])
    if owner is None:
        abort(400)

    house = House()
    house.name = request.form["name"]
    house.latitude = request.form["latitude"]
    house.longitude = request.form["longitude"]
    house.owner = owner.id

    db.session.add(house)
    db.session.commit()

    return jsonify({"creation": "success"})


@bp.route("/edit")
def edit():
    pass


@bp.route("/delete")
def delete():
    pass
