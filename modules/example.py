from flask import Blueprint, jsonify


bp = Blueprint("example", __name__, url_prefix="/example")


@bp.route("/")
def home():
    return jsonify({"test": "success"})
