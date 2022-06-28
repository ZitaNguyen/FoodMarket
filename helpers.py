import os

from flask import redirect, render_template, session
from functools import wraps


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