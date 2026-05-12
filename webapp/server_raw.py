import socket

# Step 1: Create a socket
# AF_INET = IPv4, SOCK_STREAM = TCP (stream of bytes, reliable, ordered)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Step 2: Avoid "address already in use" error on restart
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Step 3: Bind to an address and port
# "" means "listen on all network interfaces"
server_socket.bind(("", 9000))

# Step 4: Start listening. 
# 5 = maximum number of queued connections waiting to be accepted
server_socket.listen(5)

print("Server listening on port 9000...")
print("Open your browser and go to: http://localhost:9000")
print()

# Step 5: Accept one connection, then stop
connection, client_address = server_socket.accept()
# accept() BLOCKS here — the program pauses until a browser connects
# When a browser connects, it returns:
#   connection    = a new socket just for this one conversation
#   client_address = the browser's IP and port

print(f"Connection from: {client_address}")
print()

# Step 6: Read what the browser sent (up to 4096 bytes)
raw_request = connection.recv(4096)

# Step 7: Print it — first as raw bytes, then as text
print("=== RAW BYTES ===")
print(raw_request)
print()
print("=== AS TEXT ===")
print(raw_request.decode("utf-8"))

# Step 8: Close (browser will show an error — that's fine, we sent nothing back)
connection.close()
server_socket.close()