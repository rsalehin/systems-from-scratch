from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/note", methods=["POST"])
def create_note():
    # Flask parses the URL-encoded body automatically
    # request.form is a dictionary of field name → value
    title = request.form.get("title", "")
    body  = request.form.get("body", "")

    # Print to terminal so we can see what arrived
    print(f"Received note — title: '{title}', body: '{body}'")

    # For now: just show it back to the user
    return render_template("note_created.html", title=title, body=body)


@app.errorhandler(404)
def not_found(error):
    return "<h1>404 - Not Found</h1>", 404


if __name__ == "__main__":
    app.run(port=9000, debug=True)