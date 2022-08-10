from flask import session, request, redirect, render_template
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import error
from queries import query_get_seller, query_get_user, query_users, query_insert_user, query_insert_contact, query_get_last_user, query_edit_profile, query_edit_contact, query_delete_profile


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
            query_insert_user(user_details)
        else:
            user_details = (username, email, role, hash)
            query_insert_user(user_details)

        # Insert seller contact to db
        if role == "seller":
            # Ensure phone, city, district are not blank
            phone = request.form.get("phone")
            district = request.form.get("district")
            city = request.form.get("city")

            if not phone or not district or not city:
                return error("something is left empty", 400)

            last_user = query_get_last_user()
            contact_details = (district, city, phone, last_user[0])
            query_insert_contact(contact_details)

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
        session["user_about"] = user[0][5]

        return redirect("/")

    # User reached route via GET
    else:
        return render_template("login.html")


def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    return redirect("/")


def display_profile(user_id):

    user = query_get_user(user_id)
    return render_template("profile.html", user=user)


def edit_profile(user_id, user_role):
    """Edit user profile"""

    if request.method == "POST":

        user = query_get_user(user_id)

        username = request.form.get("username")
        new_password = request.form.get("new_password")
        old_password = request.form.get("old_password")
        confirmation = request.form.get("confirmation")

        # Check if username is deleted
        if not username:
            return error("username is empty", 400)

        # Check if user wanna change password
        if not new_password and not confirmation:
            hash = user[3]
        elif (new_password and not confirmation) or (not new_password and confirmation):
            return error("a password is left empty", 400)
        elif not old_password:
            return error("old password is missing", 400)
        elif not check_password_hash(user[3], old_password):
            return error("password is incorrect", 403)
        elif new_password != confirmation:
            return error("passwords do not match", 403)
        else:
            hash = generate_password_hash(new_password)

        if "about" in request.form:
            about = request.form.get("about")
            user_details = (username, hash, about, session["user_id"])
        else:
            user_details = (username, hash, session["user_id"])

        # Update user details
        query_edit_profile(user_details)

        if user_role == "buyer":
            return redirect("/profile")
        else:
            # Update seller contact details
            phone = request.form.get("phone")
            district = request.form.get("district")
            city = request.form.get("city")

            if not phone or not district or not city:
                return error("something is left empty", 400)

            contact_details = (district, city, phone, session["user_id"])
            query_edit_contact(contact_details)
            return redirect("/seller_profile")

    else:
        if user_role == "buyer":
            user = query_get_user(user_id)
        else:
            user = query_get_seller(user_id)

        return render_template("edit_profile.html", user=user, role=user_role)
