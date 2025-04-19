import sqlite3

conn = sqlite3.connect('byte_buddy.db')
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS conversations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        message TEXT NOT NULL,
        response TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')

conn.commit()
conn.close()
print("Database and table created successfully.")
