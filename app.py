import os

from flask import Flask, session, request, redirect, render_template, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

# from routes.register import register
from helpers import error, login_required, role_required
from queries import query_users, insert_user

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Make sure API key is set
# if not os.environ.get("API_KEY"):
#     raise RuntimeError("API_KEY not set")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    '''Register user'''

    if request.method == 'POST':

        username = request.form.get("username")
        email = request.form.get("email")
        role = request.form.get("role")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure all fields are not blank
        if not username or not email or not role or not password or not confirmation:
            return error("something is left empty", 400)

        # Ensure email is unique
        user = query_users(email)
        if len(user) != 0:
            return error("email already exists", 403)

        # Ensure passwords match
        if password != confirmation:
            return error("passwords do not match", 403)

        # Generate password hash and insert new user into database
        hash = generate_password_hash(password)

        if "about" in request.form:
            about = request.form.get("about")
            user_details = (username, email, role, hash, about)
            insert_user(user_details)
        else:
            user_details = (username, email, role, hash)
            insert_user(user_details)

        return redirect("/login")

    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        # Ensure username was submitted
        if not email or not password:
            return error("something is left empty", 400)

        # Query database for user
        user = query_users(email)
        print(user)

        # Ensure user exists and password is correct
        if len(user) != 1 or not check_password_hash(user[0][3], password):
            return error("invalid usernamed and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = user[0][0] # user_id

        # Remember user's role
        session["user_role"] = user[0][4]

        return redirect("/")

    # User reached route via GET
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    return redirect("/")


@app.route("/food")
@login_required
@role_required
def food():
    """Seller add their products"""

    return ("I'm a seller")



if __name__ == '__main__':
    app.run()
