from flask import Blueprint


bp = Blueprint("activity", __name__, url_prefix="/activity")


@bp.route("/start")
def start():
    pass


@bp.route("/stop")
def stop():
    pass
