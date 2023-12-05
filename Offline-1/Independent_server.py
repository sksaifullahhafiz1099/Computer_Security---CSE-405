import socket
import pickle
from ecc import *

class CustomObject:
    def __init__(self,a=0,b=0,G=(0,0),Kapub=(0,0),Kbpub=(0,0),p=0,n=0,data=[[[]]]):
        self.data = data
        self.a = a
        self.b = b
        self.G = G
        self.Kapub = Kapub
        self.Kbpub = Kbpub
        self.p = p
        self.n = n

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


        #shared----------------------------
        p = generate_prime_in_range(100000000000,500000000000)
        a = random.randrange(5,p)
        G = (random.randrange(3000,4000),random.randrange(5000,6000))
        b = G[1]**2 - G[0]**3 - G[0] * a 
        lower_limit = p + 1 - 2 * int(p**0.5)
        upper_limit = p + 1 + 2 * int(p**0.5)
        #----------------------------------
        #Alice:
        Ka = generate_prime_in_range(2, upper_limit)
        Kapub = apply_double_and_add_method(G,Ka,p,a)

        # Step 1: Server sends a custom object to the client
        initial_object = CustomObject(a,b,G,Kapub,(0, 0),p,1,[[[]]])
        client_socket.send(pickle.dumps(initial_object))

        # Step 2: Server receives a custom object from the client
        received_data = client_socket.recv(1024)
        client_object = pickle.loads(received_data)
        print(f"Received from client: {client_object.Kapub}")
        key =  apply_double_and_add_method(client_object.Kbpub,Ka,p,a)
        print("key: ",key)
        #key =  apply_double_and_add_method(client_object.Kbpub,Ka,p,a) 
        # Custom processing logic on the server
        processed_data = client_object
        print(f"Processed data: {processed_data.Kapub}")

        # Step 3: Server sends another custom object to the client
        server_response = CustomObject(processed_data)
        client_socket.send(pickle.dumps(server_response))

        client_socket.close()
        break

if __name__ == "__main__":
    start_server()
