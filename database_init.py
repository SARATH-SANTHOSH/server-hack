"""
Initializes SQLite database for security dashboard
"""

import sqlite3

db = sqlite3.connect("security.db")
cur = db.cursor()

# Alerts table
cur.execute("""
CREATE TABLE IF NOT EXISTS alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    time TEXT,
    attack TEXT,
    severity TEXT,
    explanation TEXT
)
""")

# Logs table
cur.execute("""
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    time TEXT,
    message TEXT
)
""")

db.commit()
db.close()

print("Database initialized successfully")
