import socket
import pickle

class CustomObject:
    def __init__(self, data):
        self.data = data

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'
    port = 12345
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"Server listening on {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")

        # Step 1: Server sends a custom object to the client
        initial_object = CustomObject("Hello from server!")
        client_socket.send(pickle.dumps(initial_object))

        # Step 2: Server receives a custom object from the client
        received_data = client_socket.recv(1024)
        client_object = pickle.loads(received_data)
        print(f"Received from client: {client_object.data}")

        # Custom processing logic on the server
        processed_data = client_object.data.upper()
        print(f"Processed data: {processed_data}")

        # Step 3: Server sends another custom object to the client
        server_response = CustomObject(processed_data)
        client_socket.send(pickle.dumps(server_response))

        client_socket.close()

if __name__ == "__main__":
    start_server()
