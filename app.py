from flask import Flask, render_template, request
from flask_session import Session

import users, sellers
from helpers import login_required, role_required
from queries import query_get_all_products

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
    all_products = query_get_all_products()
    starters = list(filter(lambda product: product[1] == "Starter", all_products))
    main_dishes = list(filter(lambda product: product[1] == "Main dish", all_products))
    desserts = list(filter(lambda product: product[1] == "Dessert", all_products))
    return render_template("index.html", starters=starters, main_dishes=main_dishes, desserts=desserts)


# Users register, login, logout
@app.route("/register", methods=["GET", "POST"])
def register():
    return users.register()


@app.route("/login", methods=["GET", "POST"])
def login():
    return users.login()


@app.route("/logout")
def logout():
    return users.logout()


# Sellers add, display, modify and delete product
@app.route("/add", methods=["GET", "POST"])
@login_required
@role_required
def add():
    return sellers.add_products()


@app.route("/display", methods=["GET"])
@login_required
@role_required
def display():
    return sellers.display_products()


@app.route("/modify/<string:product_id>", methods=["GET", "POST"])
@login_required
@role_required
def modify(product_id):
    return sellers.modify_product(product_id)


@app.route("/delete/<string:product_id>", methods=["POST"])
@login_required
@role_required
def delete(product_id):
    return sellers.delete_product(product_id)


if __name__ == '__main__':
    app.run()
