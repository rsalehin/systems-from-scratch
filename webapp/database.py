import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "notes.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def insert_note(title, body):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO notes (title, body) VALUES (?, ?)",
        (title, body)
    )
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return new_id

def get_all_notes():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notes ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_note(note_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notes WHERE id = ?", (note_id,))
    row = cursor.fetchone()
    conn.close()
    return row