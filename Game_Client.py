import socket

# Set the server's host and port
HEADER = 1024
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
SERVER = input()
print(SERVER)
# SERVER = "192.168.1.112"
FORMAT = 'utf-8'
disconnect_msg = "Disconnect"
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER,PORT))

# Send data to the server
message = "Hello, server! This is the client."
client.send(message.encode('utf-8'))

# Receive and print the server's response
response = client.recv(1024)
print(f"Received from server: {response.decode('utf-8')}")

# Close the connection
client.close()
