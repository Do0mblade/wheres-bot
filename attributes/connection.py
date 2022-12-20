
import sqlite3

conn = sqlite3.connect('chest.db')

cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS users(
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   first_name TEXT NOT NULL,
   user_id INTEGER NOT NULL,
   age INTEGER DEFAULT NULL,
   gender TEXT DEFAULT NULL,
   scores INT DEFAULT 0,
   admin_mode TEXT DEFAULT user,
   bonus BOOL DEFAULT False)
""")
            
cur.execute("""CREATE TABLE IF NOT EXISTS places(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    head TEXT NOT NULL,
    photo TEXT NOT NULL,
    description TEXT NOT NULL,
    price INTEGER NOT NULL,
    sale INTEGER NOT NULL,
    new_price INTEGER NOT NULL,
    site TEXT NOT NULL,
    adress TEXT NOT NULL,
    category_id INTEGER NOT NULL)
""")

cur.execute("""CREATE TABLE IF NOT EXISTS checked(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    post_id INTEGER NOT NULL)
""")

cur.execute("""CREATE TABLE IF NOT EXISTS likes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    post_id INTEGER NOT NULL)
""")

cur.execute("""CREATE TABLE IF NOT EXISTS categoryes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL)
""")

conn.commit()


