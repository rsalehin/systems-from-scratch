import socket
from parse_request import parse_http_request, print_parsed_request

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(("", 9000))
server_socket.listen(5)

print("Listening on port 9000... (Ctrl+C to stop)")
print()

# Loop forever — handle multiple requests
while True:
    connection, client_address = server_socket.accept()
    raw_request = connection.recv(4096)

    if not raw_request:
        connection.close()
        continue

    print(f"── Request from {client_address} ──")
    parsed = parse_http_request(raw_request)
    print_parsed_request(parsed)
    print()

    connection.close()