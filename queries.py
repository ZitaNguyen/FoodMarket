import sqlite3


# Queries for users

def query_users(email):
    conn = sqlite3.connect("market.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email = ?", (email,))
    users = c.fetchall()
    return users


def query_get_last_user():
    conn = sqlite3.connect("market.db")
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE id=(SELECT max(id) FROM users)")
    last_user = c.fetchone()
    return last_user


def query_insert_user(user_details):
    conn = sqlite3.connect("market.db")
    c = conn.cursor()
    sql_string = "INSERT INTO users (username, email, role, hash, about) VALUES (?, ?, ?, ?, ?)"
    c.execute(sql_string, user_details)
    conn.commit()
    conn.close()


def query_insert_contact(contact_details):
    conn = sqlite3.connect("market.db")
    c = conn.cursor()
    sql_string = ("INSERT INTO contact (district, city, phone, user_id) VALUES (?, ?, ?, ?)")
    c.execute(sql_string, contact_details)
    conn.commit()
    conn.close()


def query_get_all_products():
    conn = sqlite3.connect("market.db")
    c = conn.cursor()
    c.execute ("SELECT * FROM food")
    all_products = c.fetchall()
    return all_products


# Queries for sellers

def query_get_seller(id):
    conn = sqlite3.connect("market.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE id = ?", (id,))
    seller = c.fetchone()
    return seller

def query_get_contact(id):
    conn = sqlite3.connect("market.db")
    c = conn.cursor()
    c.execute("SELECT * FROM contact WHERE user_id = ?", (id,))
    contact = c.fetchone()
    return contact


def query_add_product(food_details):
    conn = sqlite3.connect("market.db")
    c = conn.cursor()
    sql_string = "INSERT INTO food (name, category, photo, price, description, date, user_id) VALUES (?, ?, ?, ?, ?, ?, ?)"
    c.execute(sql_string, food_details)
    conn.commit()
    conn.close()


def query_modify_product(food_details):
    conn = sqlite3.connect("market.db")
    c = conn.cursor()
    sql_string = "UPDATE food SET (name, category, photo, price, description) = (?, ?, ?, ?, ?) WHERE id = ?"
    c.execute(sql_string, food_details)
    conn.commit()
    conn.close()


def query_delete_product(product_id):
    conn = sqlite3.connect("market.db")
    c = conn.cursor()
    c.execute("DELETE FROM food WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()


def query_get_seller_products(user_id):
    conn = sqlite3.connect("market.db")
    c = conn.cursor()
    c.execute("SELECT * FROM food WHERE user_id = ?", (user_id,))
    products = c.fetchall()
    return products


def query_get_a_product(id):
    conn = sqlite3.connect("market.db")
    c = conn.cursor()
    c.execute("SELECT * FROM food WHERE id = ?", (id,))
    product = c.fetchone()
    return product