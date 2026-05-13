import sqlite3
import os
import secrets
import string

DB_PATH = os.path.join(os.path.dirname(__file__), "notes.db")

# Characters allowed in a short ID — letters and digits, no ambiguous chars
ID_ALPHABET = string.ascii_lowercase + string.digits
ID_LENGTH   = 8


def generate_short_id():
    # secrets.choice picks a cryptographically random character each time
    return "".join(secrets.choice(ID_ALPHABET) for _ in range(ID_LENGTH))


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def insert_note(title, body):
    conn   = get_connection()
    cursor = conn.cursor()

    short_id = generate_short_id()

    cursor.execute(
        "INSERT INTO notes (short_id, title, body) VALUES (?, ?, ?)",
        (short_id, title, body)
    )

    conn.commit()
    conn.close()

    # Return the short_id — this is what goes in the URL
    return short_id


def get_all_notes():
    conn   = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notes ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_note_by_short_id(short_id):
    conn   = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notes WHERE short_id = ?", (short_id,))
    row = cursor.fetchone()
    conn.close()
    return row

def delete_note(short_id):
    conn   = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM notes WHERE short_id = ?", (short_id,))

    # rowcount tells us how many rows were actually deleted
    # 0 means the short_id didn't exist
    deleted = cursor.rowcount

    conn.commit()
    conn.close()

    return deleted > 0   # True if something was deleted, False if not found