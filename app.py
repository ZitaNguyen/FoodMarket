from flask import Flask, render_template
from flask_session import Session

import users, sellers
from helpers import login_required, role_required

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
def food():
    return sellers.add_products()


@app.route("/products", methods=["GET"])
@login_required
@role_required
def products():
    return sellers.display_products()


@app.route("/modify", methods=["POST"])
@login_required
@role_required
def modify():
    return sellers.modify_product()


@app.route("/delete", methods=["POST"])
@login_required
@role_required
def delete():
    return sellers.delete_product()


if __name__ == '__main__':
    app.run()
