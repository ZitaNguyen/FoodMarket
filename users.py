from flask import session, request, redirect, render_template
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import error
from queries import query_users, insert_user


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

        # Ensure user exists and password is correct
        if len(user) != 1 or not check_password_hash(user[0][3], password):
            return error("invalid usernamed and/or password", 403)

        # Remember user's info
        session["user_id"] = user[0][0]
        session["user_name"] = user[0][1]
        session["user_role"] = user[0][4]

        return redirect("/")

    # User reached route via GET
    else:
        return render_template("login.html")


def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    return redirect("/")