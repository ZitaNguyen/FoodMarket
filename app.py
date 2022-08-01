from flask import Flask, render_template, session
from flask_session import Session

import users, sellers
from helpers import login_required, role_required
from queries import query_get_all_products, query_get_a_product, query_get_seller, query_get_seller_other_products, query_get_starters, query_get_main_dishes, query_get_desserts

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
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
    """Index page"""

    all_products = query_get_all_products()
    starters = list(filter(lambda product: product[1] == "Starter", all_products))
    main_dishes = list(filter(lambda product: product[1] == "Main dish", all_products))
    desserts = list(filter(lambda product: product[1] == "Dessert", all_products))
    return render_template("index.html", starters=starters, main_dishes=main_dishes, desserts=desserts)


@app.route("/starters", methods=["GET"])
@login_required
def starters():
    """Display all starters of all sellers"""

    starters = query_get_starters()
    return render_template("starters.html", starters=starters)


@app.route("/main_dishes", methods=["GET"])
@login_required
def main_dishes():
    """Display all main dishes of all sellers"""

    main_dishes = query_get_main_dishes()
    return render_template("main_dishes.html", main_dishes=main_dishes)


@app.route("/desserts", methods=["GET"])
@login_required
def desserts():
    """Display all desserts of all sellers"""

    desserts = query_get_desserts()
    return render_template("desserts.html", desserts=desserts)


@app.route("/product/<int:food_id>", methods=["GET"])
@login_required
def product(food_id):
    """Display product details"""

    product = query_get_a_product(food_id)
    seller = query_get_seller(product[7])
    products_from_same_seller = query_get_seller_other_products(product[7], food_id)
    return render_template("product.html", seller=seller, this_product=product, products=products_from_same_seller)


# Users register, login, logout, display profile
@app.route("/register", methods=["GET", "POST"])
def register():
    return users.register()


@app.route("/login", methods=["GET", "POST"])
def login():
    return users.login()


@app.route("/logout")
def logout():
    return users.logout()


@app.route("/profile", methods=["GET"])
@login_required
def display():
    return users.display_profile(session["user_id"])


# Sellers add, display, modify and delete product
@app.route("/add", methods=["GET", "POST"])
@login_required
@role_required
def add():
    return sellers.add_products()


@app.route("/seller_profile", methods=["GET"])
@login_required
@role_required
def display_seller():
    return sellers.display_profile(session["user_id"])


@app.route("/modify/<int:food_id>", methods=["GET", "POST"])
@login_required
@role_required
def modify(product_id):
    return sellers.modify_product(product_id)


@app.route("/delete/<int:food_id>", methods=["POST"])
@login_required
@role_required
def delete(product_id):
    return sellers.delete_product(product_id)


if __name__ == '__main__':
    app.run()
