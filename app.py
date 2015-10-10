import pkgutil
import os
from flask import Flask, Blueprint, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
import sys

app = Flask(__name__)
app.secret_key = os.urandom(24)
db = SQLAlchemy(app)
if len(sys.argv) == 2 and sys.argv[1] == "create":
    db.create_all()


def register_blueprints(package_name=None, package_path="."):
    """Register all Blueprint instances on the specified Flask application found
    in all modules for the specified package.

    :param app: the Flask application
    :param package_name: the package name
    :param package_path: the package path
    """

    for _, name, _ in pkgutil.iter_modules(package_path):
        import_string = '%s.%s' % (package_name, name) if package_name else name
        m = pkgutil.importlib.import_module(import_string)
        for item in dir(m):
            item = getattr(m, item)
            if isinstance(item, Blueprint):
                app.register_blueprint(item)

register_blueprints("modules", ["modules"])


@app.route("/")
def home():
    return jsonify({"test": "home"})


if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')
