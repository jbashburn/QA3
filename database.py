# database.py

import sqlite3

# Connect to the database (creates file if it doesn't exist)
conn = sqlite3.connect("subscribers.db")
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS subscribers (
        email TEXT UNIQUE
    )
""")
conn.commit()

def add_subscriber(email):
    try:
        cursor.execute("INSERT INTO subscribers (email) VALUES (?)", (email,))
        conn.commit()
        return True  # <-- ADDED: Return True on success
    except sqlite3.IntegrityError:
        print("Email already exists.")
        return False # <-- ADDED: Return False on duplicate error

def get_subscribers():
    cursor.execute("SELECT email FROM subscribers")
    return [row[0] for row in cursor.fetchall()]