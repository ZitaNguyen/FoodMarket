import sqlite3


# Queries for users

def query_users(email):
    conn = sqlite3.connect("market.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email = ?", (email,))
    users = c.fetchall()
    conn.close()
    return users


def query_get_user(id):
    conn = sqlite3.connect("market.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE id = ?", (id,))
    user = c.fetchone()
    conn.close()
    return user

def query_get_last_user():
    conn = sqlite3.connect("market.db")
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE id=(SELECT max(id) FROM users)")
    last_user = c.fetchone()
    conn.close()
    return last_user


def query_insert_user(user_details):
    conn = sqlite3.connect("market.db")
    c = conn.cursor()
    sql_string = "INSERT INTO users (username, email, role, hash, about) VALUES (?, ?, ?, ?, ?)"
    c.execute(sql_string, user_details)
    conn.commit()
    conn.close()


def query_edit_profile(user_details):
    conn = sqlite3.connect("market.db")
    c = conn.cursor()
    sql_string = "UPDATE users SET (username, hash, about) = (?, ?, ?) WHERE id = ?"
    c.execute(sql_string, user_details)
    conn.commit()
    conn.close()


def query_delete_profile(user_id):
    conn = sqlite3.connect("market.db")
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE id = ?", (user_id,))
    c.execute("DELETE FROM contact WHERE user_id = ?", (user_id,))
    c.execute("DELETE FROM food WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()


def query_get_search_food(query):
    conn = sqlite3.connect("market.db")
    c = conn.cursor()
    c.execute("SELECT * FROM food WHERE name LIKE ? OR name LIKE ? OR name LIKE ? OR name LIKE ? ", (query, '%'+query, query+'%', '%'+query+'%'))
    results = c.fetchall()
    conn.close()
    return results


def query_get_search_district(query):
    conn = sqlite3.connect("market.db")
    c = conn.cursor()
    c.execute("SELECT * FROM food INNER JOIN users ON food.user_id = users.id INNER JOIN contact ON users.id = contact.user_id WHERE contact.district=?", (query,))
    results = c.fetchall()
    conn.close()
    return results


# Queries for sellers

def query_get_seller(id):
    conn = sqlite3.connect("market.db")
    c = conn.cursor()
    c.execute("SELECT users.*, contact.district, contact.city, contact.phone FROM users INNER JOIN contact ON users.id = contact.user_id WHERE users.id = ?", (id,))
    seller = c.fetchone()
    conn.close()
    return seller


def query_insert_contact(contact_details):
    conn = sqlite3.connect("market.db")
    c = conn.cursor()
    sql_string = "INSERT INTO contact (district, city, phone, user_id) VALUES (?, ?, ?, ?)"
    c.execute(sql_string, contact_details)
    conn.commit()
    conn.close()


def query_edit_contact(contact_details):
    conn = sqlite3.connect("market.db")
    c = conn.cursor()
    sql_string = "UPDATE contact SET (district, city, phone) = (?, ?, ?) WHERE user_id = ?"
    c.execute(sql_string, contact_details)
    conn.commit()
    conn.close()


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
    conn.close()
    return products


def query_get_seller_other_products(user_id, food_id):
    conn = sqlite3.connect("market.db")
    c = conn.cursor()
    c.execute("SELECT * FROM food WHERE user_id = ? AND id NOT IN (?)", (user_id, food_id))
    products = c.fetchall()
    conn.close()
    return products


# Queries for food

def query_get_all_products():
    conn = sqlite3.connect("market.db")
    c = conn.cursor()
    c.execute ("SELECT * FROM food")
    all_products = c.fetchall()
    conn.close()
    return all_products


def query_get_a_product(id):
    conn = sqlite3.connect("market.db")
    c = conn.cursor()
    c.execute("SELECT * FROM food WHERE id = ?", (id,))
    product = c.fetchone()
    conn.close()
    return product


def query_get_starters():
    conn = sqlite3.connect("market.db")
    c = conn.cursor()
    c.execute("SELECT * FROM food WHERE category='Starter' ")
    starters = c.fetchall()
    conn.close()
    return starters


def query_get_main_dishes():
    conn = sqlite3.connect("market.db")
    c = conn.cursor()
    c.execute("SELECT * FROM food WHERE category='Main dish' ")
    main_dishes = c.fetchall()
    conn.close()
    return main_dishes


def query_get_desserts():
    conn = sqlite3.connect("market.db")
    c = conn.cursor()
    c.execute("SELECT * FROM food WHERE category='Dessert' ")
    desserts = c.fetchall()
    conn.close()
    return desserts