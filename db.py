#register users.db
import sqlite3

DB_NAME = 'users.db'
conn = sqlite3.connect(DB_NAME)
c = conn.cursor()
c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT 
    )""")