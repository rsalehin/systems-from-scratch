from flask import Flask, render_template, request, redirect, url_for
from database import insert_note, get_all_notes, get_note_by_short_id
from validate import validate_note
import os

app = Flask(__name__)


@app.route("/")
def home():
    notes = get_all_notes()
    return render_template("home.html", notes=notes)


@app.route("/note", methods=["POST"])
def create_note():
    title = request.form.get("title", "")
    body  = request.form.get("body", "")

    # Validate before touching the database
    errors = validate_note(title, body)

    if errors:
        # Re-render the form with error messages and the user's input preserved
        notes = get_all_notes()
        return render_template(
            "home.html",
            notes=notes,
            errors=errors,
            form_title=title,   # send back what they typed
            form_body=body
        ), 400

    short_id = insert_note(title.strip(), body.strip())
    return redirect(url_for("view_note", short_id=short_id))


@app.route("/note/<short_id>")
def view_note(short_id):
    note = get_note_by_short_id(short_id)

    if note is None:
        return render_template("not_found.html"), 404

    return render_template("note.html", note=note)


@app.errorhandler(404)
def not_found(error):
    return render_template("not_found.html"), 404


if __name__ == "__main__":
    # Read from environment, default to development settings
    debug_mode = os.environ.get("FLASK_DEBUG", "true").lower() == "true"
    port       = int(os.environ.get("PORT", "9000"))
    app.run(port=port, debug=debug_mode)