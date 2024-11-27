import socket
import threading
import sys

# Ensure the correct number of arguments
if len(sys.argv) != 3:
    print("Usage: python chat_client.py <HOST> <PORT>")
    sys.exit(1)

# Server IP and port configuration from command-line arguments
HOST = sys.argv[1]  # Server's hostname or IP address
PORT = int(sys.argv[2])  # Port to connect to

def receive_messages(client_socket):
    while True:
        try:
            # Receive and print messages from the server
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(message)
            else:
                break
        except:
            # If there's an error (like server closing), break the loop
            print("Connection closed.")
            break

def send_messages(client_socket):
    while True:
        try:
            # Take input from the user and send it to the server
            message = input("")
            client_socket.send(message.encode('utf-8'))
        except:
            print("Error sending message.")
            break

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((HOST, PORT))
        print(f"Connected to server at {HOST}:{PORT}")
    except Exception as e:
        print(f"Unable to connect to server: {e}")
        return

    # Start a thread to listen for messages from the server
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    # Start a thread to send messages to the server
    send_thread = threading.Thread(target=send_messages, args=(client_socket,))
    send_thread.start()

if __name__ == "__main__":
    main()
