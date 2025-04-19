import sqlite3

conn = sqlite3.connect('byte_buddy.db')
c = conn.cursor()

# Drop old table if needed
c.execute("DROP TABLE IF EXISTS conversations")

# Create new table without DEFAULT timestamp
c.execute('''
    CREATE TABLE conversations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        message TEXT NOT NULL,
        response TEXT NOT NULL,
        timestamp TEXT NOT NULL
    )
''')

conn.commit()
conn.close()
print("Database and table created successfully.")
