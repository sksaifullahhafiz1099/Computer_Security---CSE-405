import socket
import pickle

class CustomObject:
    def __init__(self, data):
        self.data = data

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'
    port = 12345
    client_socket.connect((host, port))

    # Step 1: Client receives a custom object from the server
    server_data = client_socket.recv(1024)
    server_object = pickle.loads(server_data)
    print(f"Received from server: {server_object.data}")

    # Custom processing logic on the client
    client_data = server_object.data * 2
    print(f"Processed data: {client_data}")

    # Step 2: Client sends another custom object to the server
    client_response = CustomObject(client_data)
    client_socket.send(pickle.dumps(client_response))

    # Step 3: Client receives another custom object from the server
    server_response_data = client_socket.recv(1024)
    server_response_object = pickle.loads(server_response_data)
    print(f"Received from server: {server_response_object.data}")

    client_socket.close()

if __name__ == "__main__":
    start_client()
