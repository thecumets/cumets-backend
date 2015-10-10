from flask import Blueprint


bp = Blueprint("session", __name__, url_prefix="/session")


@bp.route("/start")
def start():
    pass


@bp.route("/stop")
def stop():
    pass
