import socket
import pickle
from ecc import *

class CustomObject:
    def __init__(self, a=0, b=0, G=(0,0), Kapub=(0,0), Kbpub=(0,0), p=0, n=0, data=[[[]]]):
        self.data = data
        self.a = a
        self.b = b
        self.G = G
        self.Kapub = Kapub
        self.Kbpub = Kbpub
        self.p = p
        self.n = n

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'
    port = 12345
    client_socket.connect((host, port))

    # Step 1: Client receives a custom object from the server
    server_data = client_socket.recv(1024)
    server_object = pickle.loads(server_data)
    print(f"Received from server: {server_object}")

    upper_limit = server_object.p + 1 + 2 * int(server_object.p**0.5)
    # Bob
    Kb = generate_prime_in_range(2, upper_limit)
    Kbpub = apply_double_and_add_method(server_object.G, Kb, server_object.p, server_object.a)
    key = apply_double_and_add_method(server_object.Kapub, Kb, server_object.p, server_object.a)
    print("key: ",key)
    # Custom processing logic on the client
    # Construct a new CustomObject with the necessary information
    client_data = CustomObject(
        a=server_object.a,
        b=server_object.b,
        G=server_object.G,
        Kapub=server_object.Kapub,
        Kbpub=Kbpub,
        p=server_object.p,
        n=1,  # Adjust n as needed
        data=[[[0]]]  # Adjust data as needed
    )
    print(f"Processed data: {client_data}")

    # Step 2: Client sends another custom object to the server
    client_socket.send(pickle.dumps(client_data))

    # Step 3: Client receives another custom object from the server
    server_response_data = client_socket.recv(1024)
    server_response_object = pickle.loads(server_response_data)
    print(f"Received from server: {server_response_object}")

    client_socket.close()

if __name__ == "__main__":
    start_client()
