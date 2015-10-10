from functools import wraps
from flask import session, abort


def requires_user(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        try:
            assert(session["user_id"] is not None)
        except (AssertionError, KeyError):
            abort(401)
        return f(*args, **kwargs)
    return decorator
