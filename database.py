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

# --- CREATE ---
def add_subscriber(email):
    """Adds a new email to the database."""
    try:
        cursor.execute("INSERT INTO subscribers (email) VALUES (?)", (email,))
        conn.commit()
        return True  # Return True on success
    except sqlite3.Error as e: # Catches IntegrityError (duplicate) and others
        print(f"Error adding {email}: {e}")
        return False

# --- READ ---
def get_subscribers():
    """Gets a list of all subscriber emails."""
    try:
        cursor.execute("SELECT email FROM subscribers")
        return [row[0] for row in cursor.fetchall()]
    except sqlite3.Error as e:
        print(f"Error fetching subscribers: {e}")
        return []

# --- UPDATE ---
def edit_subscriber(old_email, new_email):
    """Updates an email address in the database."""
    try:
        cursor.execute("UPDATE subscribers SET email = ? WHERE email = ?", (new_email, old_email))
        conn.commit()
        return cursor.rowcount > 0 # True if a row was updated
    except sqlite3.Error as e: # Catches IntegrityError (duplicate new_email)
        print(f"Error updating {old_email}: {e}")
        return False

# --- DELETE ---
def delete_subscriber(email):
    """Deletes a subscriber from the database."""
    try:
        cursor.execute("DELETE FROM subscribers WHERE email = ?", (email,))
        conn.commit()
        return cursor.rowcount > 0 # True if a row was deleted
    except sqlite3.Error as e:
        print(f"Error deleting {email}: {e}")
        return False