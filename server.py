import socket
import sys
import threading

# Server IP and port configuration
HOST = '127.0.0.1'  # localhost
PORT = int(sys.argv[1])  # Port to listen on (non-privileged ports are > 1023)

# List to store connected client sockets
clients = []


# Function to broadcast messages to all connected clients
def broadcast(message, _client_socket):
    for client in clients:
        if client != _client_socket:
            try:
                client.send(message)
            except:
                # If the client connection is broken, remove it from the list
                client.close()
                clients.remove(client)


# Function to handle client messages
def handle_client(client_socket):
    while True:
        try:
            # Receive message from client
            message = client_socket.recv(1024)
            if message:
                print(f"Received message: {message.decode('utf-8')}")
                broadcast(message, client_socket)
            else:
                break
        except:
            break

    # If client disconnects, remove from the client list
    client_socket.close()
    clients.remove(client_socket)
    print("Client disconnected")


# Main function to start the chat server
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Server started on {HOST}:{PORT}")

    while True:
        # Accept new client connections
        client_socket, client_address = server_socket.accept()
        print(f"New connection from {client_address}")

        # Add the new client to the list of clients
        clients.append(client_socket)

        # Start a new thread to handle the client
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

if __name__ == "__main__":
    start_server()