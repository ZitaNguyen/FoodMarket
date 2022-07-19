import os

from flask import request, redirect, render_template, session
from werkzeug.utils import secure_filename
from datetime import datetime

from helpers import error, allowed_file
from queries import insert_food, query_seller_products


def add_products():
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
            UPLOAD_FOLDER = 'static/photos'
            photo.save(os.path.join(UPLOAD_FOLDER, secure_filename(photo.filename)))
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


def display_products():
    """Display all seller's products"""

    products = query_seller_products(session["user_id"])

    # filter by category

    return render_template("products.html", products=products)