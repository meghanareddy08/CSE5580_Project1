import socket
import threading
import sys

class Node:
    def __init__(self, node_id, server_host='localhost', server_port=5555):
        self.node_id = node_id
        self.server_host = server_host
        self.server_port = server_port
        self.socket = None

    def start(self):
        # Connect to the server
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.server_host, self.server_port))
            print(f"Node {self.node_id} connected to the server")
            
            # Send the node ID to the server
            self.socket.sendall(str(self.node_id).encode())
            
            # Listen for incoming messages from the server
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.start()
            
            # Example: Send data to other nodes
            self.send_data()
            
        except ConnectionRefusedError:
            print("Connection to the server failed. Make sure the server is running.")
            sys.exit(1)

    def receive_messages(self):
        while True:
            try:
                data = self.socket.recv(1024)
                if not data:
                    break
                print(f"Node {self.node_id} received: {data.decode()}")
            except ConnectionResetError:
                break

    def send_data(self):
        # Example method to send data to other nodes
        while True:
            message = input(f"Node {self.node_id} - Enter message: ")
            self.socket.sendall(message.encode())

    def shutdown(self):
        # Close the node socket
        if self.socket:
            self.socket.close()
