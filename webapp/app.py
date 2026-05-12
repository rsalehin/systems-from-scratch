from flask import Flask, render_template, request
import os

app = Flask(__name__)


@app.route("/")
def home():
    # Pass data into the template as keyword arguments
    return render_template("home.html", visitor_ip=request.remote_addr)


@app.route("/about")
def about():
    return render_template("about.html")


@app.errorhandler(404)
def not_found(error):
    return "<h1>404 - Not Found</h1>", 404


if __name__ == "__main__":
    app.run(port=9000, debug=True)