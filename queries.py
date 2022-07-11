import sqlite3


def query_users(email):
    conn = sqlite3.connect("market.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email = ?", (email,))
    users = c.fetchall()
    return users


def insert_user(user_details):
    conn = sqlite3.connect("market.db")
    c = conn.cursor()
    sql_string = "INSERT INTO users (username, email, role, hash, about) VALUES (?, ?, ?, ?, ?)"
    c.execute(sql_string, user_details)
    conn.commit()
    conn.close()


def insert_food(food_details):
    conn = sqlite3.connect("market.db")
    c = conn.cursor()
    sql_string = "INSERT INTO food (name, category, photo, price, description, date, user_id) VALUES (?, ?, ?, ?, ?, ?, ?)"
    c.execute(sql_string, food_details)
    conn.commit()
    conn.close()

def query_seller_products(user_id):
    conn = sqlite3.connect("market.db")
    c = conn.cursor()
    c.execute("SELECT * FROM food WHERE user_id = ?", (user_id,))
    products = c.fetchall()
    return products