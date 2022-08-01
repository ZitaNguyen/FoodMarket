import os

from flask import request, redirect, render_template, session
from werkzeug.utils import secure_filename
from datetime import datetime

from helpers import error, allowed_file
from queries import query_add_product, query_modify_product, query_delete_product, query_get_a_product, query_get_seller_products, query_get_seller


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
        query_add_product(food_details)

        return redirect("/display")

    else:
        return render_template("add_product.html")


def display_profile(seller_id):
    """Display all seller's products"""

    seller = query_get_seller(seller_id)
    products = query_get_seller_products(seller_id)
    starters = list(filter(lambda product: product[1] == "Starter", products))
    main_dishes = list(filter(lambda product: product[1] == "Main dish", products))
    desserts = list(filter(lambda product: product[1] == "Dessert", products))

    return render_template("seller_profile.html", seller=seller, starters=starters, main_dishes=main_dishes, desserts=desserts)


def modify_product(product_id):
    """Modify information of existing product"""

    # Get existing product
    product = query_get_a_product(product_id)

    if request.method == "POST":

        name = request.form.get("food-name")
        category = request.form.get("food-category")
        price = request.form.get("food-price")
        if request.form.get("food-description") == '':
            description = product[4]
        else:
            description = request.form.get("food-description")

        # Check if modify photo
        photo = request.files["food-photo"]
        if photo.filename == '':
            url_photo = product[3]
        else: # Upload new photo
            if photo and allowed_file(photo.filename):
                UPLOAD_FOLDER = 'static/photos'
                photo.save(os.path.join(UPLOAD_FOLDER, secure_filename(photo.filename)))
                url_photo = photo.filename
            else:
                return error("file format is not allowed", 400)

        food_details = (name, category, url_photo, price, description, product_id)
        query_modify_product(food_details)

        return redirect("/display")

    else:

        return render_template("modify_product.html", product=product)


def delete_product(product_id):
    """Delete an existing product"""

    query_delete_product(product_id)

    return redirect("/display")