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