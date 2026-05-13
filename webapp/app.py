from flask import Flask, render_template, request, redirect, url_for, jsonify
from database import insert_note, get_all_notes, get_note_by_short_id
from validate import validate_note
from logger import logger
import os, time
from flask import g

app = Flask(__name__)


@app.before_request
def before_request():
    g.start_time = time.time()
    logger.info(f"→ {request.method} {request.path}  from {request.remote_addr}")


@app.after_request
def after_request(response):
    duration_ms = (time.time() - g.start_time) * 1000
    logger.info(f"← {response.status_code}  {duration_ms:.1f}ms")
    return response


@app.route("/")
def home():
    notes = get_all_notes()
    logger.debug(f"home: loaded {len(notes)} notes")
    return render_template("home.html", notes=notes)


@app.route("/note", methods=["POST"])
def create_note():
    title = request.form.get("title", "")
    body  = request.form.get("body", "")

    errors = validate_note(title, body)

    if errors:
        logger.warning(f"validation failed: {errors}  title='{title[:50]}'")
        # Return JSON error so JavaScript can show it
        return jsonify({"ok": False, "errors": errors}), 400

    short_id = insert_note(title.strip(), body.strip())
    logger.info(f"note created: short_id={short_id}  title='{title.strip()[:50]}'")

    # Return JSON with the new note's data
    return jsonify({
        "ok":       True,
        "short_id": short_id,
        "title":    title.strip(),
    }), 201  # 201 = Created


@app.route("/note/<short_id>")
def view_note(short_id):
    note = get_note_by_short_id(short_id)
    if note is None:
        logger.warning(f"note not found: short_id={short_id}")
        return render_template("not_found.html"), 404
    logger.debug(f"note viewed: short_id={short_id}")
    return render_template("note.html", note=note)


@app.errorhandler(404)
def not_found(error):
    logger.warning(f"404: {request.path}")
    return render_template("not_found.html"), 404


@app.errorhandler(500)
def server_error(error):
    logger.error(f"500: {error}", exc_info=True)
    return "<h1>Something went wrong.</h1>", 500


if __name__ == "__main__":
    debug_mode = os.environ.get("FLASK_DEBUG", "true").lower() == "true"
    port       = int(os.environ.get("PORT", "9000"))
    logger.info(f"starting webapp on port {port}  debug={debug_mode}")
    app.run(port=port, debug=debug_mode)