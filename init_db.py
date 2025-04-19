import sqlite3

conn = sqlite3.connect('byte_buddy.db')  # Make sure this matches your actual DB name
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
''')

conn.commit()
conn.close()

print("✅ users table created.")
