from flask import redirect, render_template, session
from functools import wraps
from uuid import uuid4


def error(message, code):
    """Render error message to user."""

    return render_template("error.html", message=message, code=code)


def login_required(f):
    """Decorate routes to require login."""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def role_required(f):
    """Decorate routes to require role seller."""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_role") != "seller":
            return redirect("/")
        return f(*args, **kwargs)

    return decorated_function


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def make_unique(string):
    ident = uuid4().__str__()
    return f"{ident}-{string}"