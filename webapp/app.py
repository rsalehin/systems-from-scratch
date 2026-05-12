from flask import Flask, render_template, request, redirect, url_for
from database import insert_note, get_all_notes, get_note

app = Flask(__name__)


@app.route("/")
def home():
    notes = get_all_notes()
    return render_template("home.html", notes=notes)


@app.route("/note", methods=["POST"])
def create_note():
    title = request.form.get("title", "").strip()
    body  = request.form.get("body", "").strip()

    if not title or not body:
        return "Title and body are required.", 400

    new_id = insert_note(title, body)

    # Redirect to the new note's page
    return redirect(url_for("view_note", note_id=new_id))


@app.route("/note/<int:note_id>")
def view_note(note_id):
    note = get_note(note_id)
    if note is None:
        return "<h1>Note not found</h1>", 404
    return render_template("note_created.html", title=note["title"], body=note["body"])


@app.errorhandler(404)
def not_found(error):
    return "<h1>404 - Not Found</h1>", 404


if __name__ == "__main__":
    app.run(port=9000, debug=True)