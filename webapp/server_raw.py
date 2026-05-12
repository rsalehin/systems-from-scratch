import socket
from parse_request import parse_http_request, print_parsed_request

def build_http_response(status_code, status_text, body, content_type="text/html"):
    # The body must be encoded to bytes to measure its length accurately
    body_bytes = body.encode("utf-8")

    # Build response line by line
    # Every line MUST end with \r\n — the HTTP spec requires it
    response = (
        f"HTTP/1.1 {status_code} {status_text}\r\n"
        f"Content-Type: {content_type}; charset=utf-8\r\n"
        f"Content-Length: {len(body_bytes)}\r\n"
        f"\r\n"  # ← blank line: end of headers
    )

    # Return headers as bytes + body as bytes
    return response.encode("utf-8") + body_bytes


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(("", 9000))
server_socket.listen(5)

print("Listening on port 9000...")
print()

while True:
    connection, client_address = server_socket.accept()
    raw_request = connection.recv(4096)

    if not raw_request:
        connection.close()
        continue

    parsed = parse_http_request(raw_request)
    print(f"── {parsed['method']} {parsed['path']} ──")

    # ── Route based on path ───────────────────────────────
    if parsed["path"] == "/":
        body = """
        <html>
          <body>
            <h1>Hello from your handmade server</h1>
            <p>You built this from a raw TCP socket.</p>
            <a href="/about">Go to About</a>
          </body>
        </html>
        """
        response = build_http_response(200, "OK", body)

    elif parsed["path"] == "/about":
        body = """
        <html>
          <body>
            <h1>About</h1>
            <p>This server speaks HTTP with no framework.</p>
            <a href="/">Go home</a>
          </body>
        </html>
        """
        response = build_http_response(200, "OK", body)

    else:
        body = """
        <html>
          <body>
            <h1>404 - Not Found</h1>
            <p>There is nothing at this path.</p>
          </body>
        </html>
        """
        response = build_http_response(404, "Not Found", body)

    connection.sendall(response)
    connection.close()