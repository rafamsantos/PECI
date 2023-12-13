import socket

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Get the server's hostname and port
server_host = socket.gethostname()
server_port = 9999

# Connect to the server
client_socket.connect((server_host, server_port))

# Receive data from the server
response = client_socket.recv(1024)
print(f"Server says: {response.decode()}")

# Close the connection
#client_socket.close()
