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
        #print(f"Received from client: {client_object.Kapub}")
        key_alice =  apply_double_and_add_method(client_object.Kbpub,Ka,p,a)
        print("key: ",key_alice)
        #key =  apply_double_and_add_method(client_object.Kbpub,Ka,p,a) 
        # Custom processing logic on the server
        #---------------------------------------

        from aes import AES
        from key import Key
        from util import Util

        def encrypt(message,key):
            for i in range(11):
                if i == 0:
                    message = aes.add_round_key(message,key) 
                if i <= 9 and i > 0:
                    message = aes.substitute_bytes(message)
                    message = aes.shift_row(message)
                    message = aes.mix_columns(message)  
                    message = aes.add_round_key(message,key)
                if i == 10:
                    message = aes.substitute_bytes(message) 
                    message = aes.shift_row(message)
                    message = aes.add_round_key(message,key) 
                if i < 10:
                    key = keyExpand.expand(key,i)
            return message

        util = Util()
        aes = AES()
        keyExpand = Key()

        IV = [
                [0x33, 0xf1, 0x04, 0x2b], 
                [0x00, 0x12, 0xb3, 0x68],
                [0xf5, 0xa0, 0x10, 0x3e],
                [0xf1, 0xbb, 0x19, 0x87]
            ]

        #taking massage and creating string chunk array
        message = input("Enter something: ")
        padded_input = util.pad_input(message)
        input_chunks = util.chunk_string(padded_input)

        #taking key and creating chunk array(only first one will be used)
        #user_key =input("Enter a Key: ")
        user_key = key_alice
        padded_key = util.pad_input(user_key)
        key_chunks = util.chunk_string(padded_key)

        #only the first chunk is taken as the key matrix
        key = util.string_to_matrix(key_chunks[0])

        #-----------------------------------------------
        """
        message = util.string_to_matrix(input_chunks[0])
        plain_message = list(map(list, zip(*message)))
        encrypted_message = encrypt(plain_message,key)
        encrypted_message = list(map(list, zip(*encrypted_message)))
        util.print_mat(encrypted_message)
        print(util.matrix_to_string(encrypted_message))
        """
        print(input_chunks)

        cipher_blocks = [[[0] * 4 for _ in range(4)] for _ in range(len(input_chunks))]
        for i in range(len(input_chunks)):
            P = util.string_to_matrix(input_chunks[i])
            P = list(map(list, zip(*P)))
            #util.print_mat(P)
            if i == 0:
                cipher_blocks[0] = encrypt(util.xor(IV,P),key)
                cipher_blocks[0] = list(map(list, zip(*cipher_blocks[0])))
                print(util.print_mat(cipher_blocks[0]))
            else:
                cipher_blocks[i] = encrypt(util.xor(cipher_blocks[i-1],P),key)
                cipher_blocks[i] = list(map(list, zip(*cipher_blocks[i])))

        #printing cipher strings        
        #cipher_string = util.matrix_list_to_string_inv(cipher_blocks)
        #print(cipher_string)
        #util.print_mat(cipher_blocks[0])

        for element in cipher_blocks:
            util.print_mat(element)

        
        client_object.data = cipher_blocks
        #---------------------------------------
        processed_data = client_object
        #print(f"Processed data: {processed_data.Kapub}")

        # Step 3: Server sends another custom object to the client
        server_response = CustomObject(processed_data)
        client_socket.send(pickle.dumps(server_response))

        client_socket.close()
        break

if __name__ == "__main__":
    start_server()
