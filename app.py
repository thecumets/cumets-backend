import pkgutil
from flask.ext.httpauth import HTTPBasicAuth
import os
from flask import Flask, Blueprint, jsonify, g
from database import db
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand


app = Flask(__name__)
app.config.from_object('config')
app.secret_key = os.urandom(24)
db.init_app(app)
db.app = app
migrate = Migrate(app, db)
auth = HTTPBasicAuth()

manager = Manager(app)
manager.add_command('db', MigrateCommand)


@auth.verify_password
def verify_password(facebook_id_or_token, password):
    from models import User
    # first try to authenticate by token
    user = User.verify_auth_token(facebook_id_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(facebook_id=facebook_id_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


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
    import sys

    if len(sys.argv) == 2 and sys.argv[1] == "create":
        from database import db
        from models import *
        db.create_all()
    else:
        manager.run()
        # app.run(debug=True, port=5000, host='0.0.0.0')
