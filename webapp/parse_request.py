def parse_http_request(raw_bytes):
    # Decode bytes to a string
    raw_text = raw_bytes.decode("utf-8")

    # Split the entire request into lines
    # HTTP uses \r\n as the line separator
    lines = raw_text.split("\r\n")

    # ── LINE 1: the request line ──────────────────────────
    # e.g. "GET /about HTTP/1.1"
    request_line = lines[0]
    parts = request_line.split(" ")
    method  = parts[0]   # "GET", "POST", etc.
    path    = parts[1]   # "/", "/about", "/submit"
    version = parts[2]   # "HTTP/1.1"

    # ── LINES 2+: headers ─────────────────────────────────
    headers = {}
    body_start_index = 0

    for i, line in enumerate(lines[1:], start=1):
        if line == "":
            # Blank line = end of headers
            # Body starts on the next line
            body_start_index = i + 1
            break

        # Each header looks like "Key: Value"
        colon_pos = line.index(":")
        key   = line[:colon_pos].strip()
        value = line[colon_pos + 1:].strip()
        headers[key] = value

    # ── BODY ──────────────────────────────────────────────
    # Everything after the blank line, joined back together
    body = "\r\n".join(lines[body_start_index:]).strip()

    return {
        "method":  method,
        "path":    path,
        "version": version,
        "headers": headers,
        "body":    body,
    }


# ── Pretty printer ────────────────────────────────────────
def print_parsed_request(parsed):
    print(f"  Method  : {parsed['method']}")
    print(f"  Path    : {parsed['path']}")
    print(f"  Version : {parsed['version']}")
    print()
    print("  Headers:")
    for key, value in parsed["headers"].items():
        print(f"    {key}: {value}")
    if parsed["body"]:
        print()
        print(f"  Body: {parsed['body']}")