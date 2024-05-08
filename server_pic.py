import socket

# Server configuration
HOST = '192.168.26.27'  # Listen on all network interfaces
PORT = 12345      # Port to listen on

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address and port
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen(1)
print("Server listening on port", PORT)

# Accept a connection
client_socket, client_address = server_socket.accept()
print("Connected to:", client_address)

while True:
    while True:
        # Receive data from the client
        data = client_socket.recv(1024)
        if not data:
            break  # No more data received, end the connection
        print("Received:", data.decode())



