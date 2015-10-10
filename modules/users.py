from flask import Blueprint


bp = Blueprint("users", __name__, url_prefix="/users")


@bp.route("/create")
def create():
    pass


@bp.route("/login")
def login():
    pass
