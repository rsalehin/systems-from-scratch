import psycopg2
import psycopg2.extras
import os
import secrets
import string

# Connection string — reads from environment variable with a development default
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://notesuser:notespass@localhost:5432/notesapp"
)

ID_ALPHABET = string.ascii_lowercase + string.digits
ID_LENGTH   = 8


def generate_short_id():
    return "".join(secrets.choice(ID_ALPHABET) for _ in range(ID_LENGTH))


def get_connection():
    # psycopg2.connect() opens a TCP connection to the PostgreSQL server
    # cursor_factory makes rows behave like dictionaries — same as sqlite3.Row
    conn = psycopg2.connect(DATABASE_URL)
    conn.cursor_factory = psycopg2.extras.RealDictCursor
    return conn


def insert_note(title, body):
    conn   = get_connection()
    cursor = conn.cursor()

    short_id = generate_short_id()

    # PostgreSQL uses %s placeholders instead of SQLite's ?
    # Everything else is identical
    cursor.execute(
        "INSERT INTO notes (short_id, title, body) VALUES (%s, %s, %s)",
        (short_id, title, body)
    )

    conn.commit()
    conn.close()

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
    cursor.execute("SELECT * FROM notes WHERE short_id = %s", (short_id,))
    row = cursor.fetchone()
    conn.close()
    return row


def delete_note(short_id):
    conn   = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notes WHERE short_id = %s", (short_id,))
    deleted = cursor.rowcount
    conn.commit()
    conn.close()
    return deleted > 0