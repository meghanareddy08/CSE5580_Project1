import socket
import threading
import queue

class Server:
    def __init__(self, host='localhost', port=5555):
        self.host = host
        self.port = port
        self.socket = None
        self.clients = {}  # Dictionary to keep track of connected clients
        self.frame_buffer = queue.Queue()  # Global frame buffer for incoming packets

    def start(self):
        # Create a socket for server
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen()

        print(f"Server started on {self.host}:{self.port}")

        # Accept incoming connections and spawn threads to handle them
        while True:
            client_socket, client_address = self.socket.accept()
            print(f"New connection from {client_address}")
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
            client_thread.start()

    def handle_client(self, client_socket, client_address):
        # Add client to the dictionary
        self.clients[client_address] = client_socket

        while True:
            try:
                # Receive data from the client
                data = client_socket.recv(1024)
                if not data:
                    break
                
                # Put the received packet into the frame buffer
                self.frame_buffer.put((client_address, data))
                
                # Process the data (forward to appropriate client or do other operations)
                self.process_data(client_address, data)
            except ConnectionResetError:
                break

        # Close the client socket and remove from the dictionary
        print(f"Connection closed with {client_address}")
        client_socket.close()
        del self.clients[client_address]

    def process_data(self, sender_address, data):
        # Implement your logic to process incoming data here
        # For example, forward the data to the appropriate recipient client based on the table
        pass

    def shutdown(self):
        # Close the server socket
        if self.socket:
            self.socket.close()
