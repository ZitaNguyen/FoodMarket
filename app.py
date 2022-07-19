import os

from flask import Flask, session, request, redirect, render_template
from flask_session import Session
from werkzeug.utils import secure_filename
from datetime import datetime

import users
from helpers import error, login_required, role_required, allowed_file
from queries import query_seller_products, query_users, insert_user, insert_food

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
UPLOAD_FOLDER = 'static/photos'
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
Session(app)


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
    return users.register()


@app.route("/login", methods=["GET", "POST"])
def login():
    return users.login()


@app.route("/logout")
def logout():
    return users.logout()


@app.route("/food", methods=["GET", "POST"])
@login_required
@role_required
def add():
    """Seller add their products"""

    if request.method == "POST":

        name = request.form.get("food-name")
        category = request.form.get("food-category")
        price = request.form.get("food-price")
        description = request.form.get("food-description")
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        # Upload photo
        photo = request.files["food-photo"]

        if photo.filename == '':
            return error("no selected file", 400)

        if photo and allowed_file(photo.filename):
            photo.save(os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(photo.filename)))
            url_photo = photo.filename
        else:
            return error("file format is not allowed", 400)

        # Ensure all fields are not blank
        if not name or not category or not price or not description:
            return error("something is left empty", 400)

        food_details = (name, category, url_photo, price, description, now, session["user_id"])
        insert_food(food_details)

        return redirect("/products")

    else:
        return render_template("food.html")


@app.route("/products", methods=["GET"])
@login_required
@role_required
def display():
    """Display all seller's products"""

    products = query_seller_products(session["user_id"])

    # filter by category

    return render_template("products.html", products=products)


if __name__ == '__main__':
    app.run()
