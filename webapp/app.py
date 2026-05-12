from flask import Flask, request

# Flask takes __name__ so it knows where your project files are
app = Flask(__name__)


# This decorator registers "/" as a route
# When a GET request arrives for "/", Flask calls this function
@app.route("/")
def home():
    return """
    <html>
      <body>
        <h1>Hello from Flask</h1>
        <p>Flask is handling the socket, parsing, and response building.</p>
        <a href="/about">Go to About</a>
      </body>
    </html>
    """


@app.route("/about")
def about():
    return """
    <html>
      <body>
        <h1>About</h1>
        <p>Same server. Less plumbing.</p>
        <a href="/">Go home</a>
      </body>
    </html>
    """


# Flask handles 404 automatically — but you can customize it
@app.errorhandler(404)
def not_found(error):
    return "<h1>404 - Not Found</h1>", 404


if __name__ == "__main__":
    # debug=True: auto-restarts when you save the file
    # Shows detailed errors in the browser
    app.run(port=9000, debug=True)