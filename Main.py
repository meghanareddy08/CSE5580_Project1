import threading
import sys
from server import Server
from Node import Node

class Main:
    def __init__(self, node_count):
        self.server = None
        self.nodes = []
        self.node_count = node_count

    def start(self):
        # Instantiate the server
        self.server = Server()  # Instantiate your server object here

        # Start the server in a separate thread
        server_thread = threading.Thread(target=self.server.start)
        server_thread.start()

        # Instantiate nodes based on the provided count
        for i in range(1, self.node_count + 1):
            node = Node(node_id=i)  # Instantiate your node object here
            self.nodes.append(node)

        # Start nodes in separate threads
        node_threads = []
        for node in self.nodes:
            node_thread = threading.Thread(target=node.start)
            node_threads.append(node_thread)
            node_thread.start()

        # Wait for all nodes to finish sending data
        for node_thread in node_threads:
            node_thread.join()

        # Shut down all nodes
        for node in self.nodes:
            node.shutdown()

        # Shut down the server
        self.server.shutdown()

        # Exit cleanly
        sys.exit(0)

if __name__ == "__main__":
    # Parse command line arguments to get the number of nodes
    if len(sys.argv) != 2:
        print("Usage: python main.py <number_of_nodes>")
        sys.exit(1)

    try:
        node_count = int(sys.argv[1])
    except ValueError:
        print("Invalid number of nodes. Please provide an integer value.")
        sys.exit(1)

    # Instantiate and start the main class
    main = Main(node_count)
    main.start()
