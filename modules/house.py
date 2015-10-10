from flask import Blueprint


bp = Blueprint("house", __name__, url_prefix="/house")


@bp.route("/create")
def create():
    pass


@bp.route("/edit")
def edit():
    pass


@bp.route("/delete")
def delete():
    pass
