import pkgutil
import os
from flask import Flask, Blueprint, jsonify


# https://github.com/mattupstate/overholt/blob/master/overholt/helpers.py (MIT license)
def register_blueprints(app, package_name=None, package_path="."):
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


def create_app():
    """Creates an app by registering blueprints in the modules directory
    and loading the configuration
    """
    app = Flask(__name__)
    app.secret_key = os.urandom(24)
    register_blueprints(app, "modules", ["modules"])

    @app.route("/")
    def home():
        return jsonify({"test": "home"})

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)
