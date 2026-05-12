import sqlite3
import os

# Path to the database file — same folder as this script
DB_PATH = os.path.join(os.path.dirname(__file__), "notes.db")

def get_connection():
    # Open the database file
    # If the file doesn't exist, SQLite creates it automatically
    conn = sqlite3.connect(DB_PATH)

    # Make rows behave like dictionaries instead of plain tuples
    # So you can do row["title"] instead of row[0]
    conn.row_factory = sqlite3.Row

    return conn


# ── INSERT ────────────────────────────────────────────────
def insert_note(title, body):
    conn = get_connection()
    cursor = conn.cursor()

    # The ? marks are placeholders — never put variables directly in SQL strings
    # (that's how SQL injection attacks happen)
    cursor.execute(
        "INSERT INTO notes (title, body) VALUES (?, ?)",
        (title, body)
    )

    # lastrowid = the id the database assigned to this new row
    new_id = cursor.lastrowid

    conn.commit()   # Write the change to disk permanently
    conn.close()

    return new_id


# ── SELECT ALL ────────────────────────────────────────────
def get_all_notes():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM notes ORDER BY created_at DESC")

    # fetchall() returns a list of Row objects
    rows = cursor.fetchall()

    conn.close()
    return rows


# ── SELECT ONE ────────────────────────────────────────────
def get_note(note_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM notes WHERE id = ?", (note_id,))

    # fetchone() returns a single Row, or None if not found
    row = cursor.fetchone()

    conn.close()
    return row


# ── TEST IT ───────────────────────────────────────────────
if __name__ == "__main__":
    print("Inserting a note from Python...")
    new_id = insert_note("From Python", "This row was inserted by Python code.")
    print(f"New row id: {new_id}")
    print()

    print("All notes:")
    for row in get_all_notes():
        print(f"  [{row['id']}] {row['title']} — {row['created_at']}")
    print()

    print(f"Fetching note id={new_id}:")
    note = get_note(new_id)
    if note:
        print(f"  Title: {note['title']}")
        print(f"  Body:  {note['body']}")
    else:
        print("  Not found.")