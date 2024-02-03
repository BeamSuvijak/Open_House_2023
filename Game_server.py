import socket
import threading

def handle_client(client_socket, address):
    print(f"Connection from {address}")

    while True:
        data = client_socket.recv(1024)
        if not data:
            break

        print(f"Received data from {address}: {data.decode('utf-8')}")

        # Add your processing logic here

        response = "Hello, client! This is the server."
        client_socket.send(response.encode('utf-8'))

    print(f"Connection with {address} closed")
    client_socket.close()

# Set the host and port
HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
disconnect_msg = "Disconnect"
SERVER = socket.gethostbyname(socket.gethostname())
print(SERVER)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER,PORT))

# Listen for incoming connections
server.listen()

print(f"Server listening on {SERVER}:{PORT}")

while True:
    # Wait for a connection from a client
    client_socket, client_address = server.accept()

    # Create a new thread to handle the client
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()
