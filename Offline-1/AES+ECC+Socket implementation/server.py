import socket
import pickle
import time
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


        #shared-variables----------------------------
        start_time_key = time.time()
        p = generate_prime_in_range(100000000000,500000000000)
        a = random.randrange(5,p)
        G = (random.randrange(3000,4000),random.randrange(5000,6000))
        b = G[1]**2 - G[0]**3 - G[0] * a 
        lower_limit = p + 1 - 2 * int(p**0.5)
        upper_limit = p + 1 + 2 * int(p**0.5)
        #-------------------------------------------
        #Alice generating Kapub:
        Ka = generate_prime_in_range(2, upper_limit)
        Kapub = apply_double_and_add_method(G,Ka,p,a)

        # Step 1: Server Alice sends a Kapub to the client Bob
        initial_object = CustomObject(a,b,G,Kapub,(0, 0),p,1,[[[]]])
        client_socket.send(pickle.dumps(initial_object))

        # Step 2: Server Alice receives a Kbpub from the client Bob
        received_data = client_socket.recv(1024)
        client_object = pickle.loads(received_data)
        
        #Alice generating key
        key_alice =  apply_double_and_add_method(client_object.Kbpub,Ka,p,a)
        end_time_key = time.time()
        print("Alice's key int: ",key_alice[0])
    
        #AES encryption process with CBC
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


        #taking key and creating chunk array(only first one will be used)
        #user_key =input("Enter a Key: ") #not taken, created using ecc
        hex_values = [hex(ord(char))[2:] for char in str(key_alice[0])]
        hex_string = ''.join(hex_value.zfill(2) for hex_value in hex_values)
        user_key = hex_string
        padded_key = util.pad_input(user_key)
        key_chunks = util.chunk_string(padded_key)

        #only the first chunk is taken as the key matrix
        key = util.string_to_matrix(key_chunks[0])

        #taking massage and creating string chunk array
        message = input("Enter something: ")
        padded_input = util.pad_input(message)
        input_chunks = util.chunk_string(padded_input)

        #-----------------------------------------------
        print("")
        print("key:")
        print("In ASCII: ",key_chunks[0])
        print("In HEX: ",util.string_to_hex_pairs(key_chunks[0]))
        print("")
        print("Plain Text:")
        print("In ASCII: ",message)
        print("In HEX: ",util.string_to_hex_pairs(message))
        #-----------------------------------------------

        #AES
        start_time_encryption = time.time()
        cipher_blocks = [[[0] * 4 for _ in range(4)] for _ in range(len(input_chunks))]
        for i in range(len(input_chunks)):
            P = util.string_to_matrix(input_chunks[i])
            P = list(map(list, zip(*P)))
            #util.print_mat(P)
            if i == 0:
                cipher_blocks[0] = encrypt(util.xor(IV,P),key)
                cipher_blocks[0] = list(map(list, zip(*cipher_blocks[0])))
            else:
                cipher_blocks[i] = encrypt(util.xor(cipher_blocks[i-1],P),key)
                cipher_blocks[i] = list(map(list, zip(*cipher_blocks[i])))
        end_time_encryption = time.time()
   
        client_object.data = cipher_blocks
        print("")
        print("Ciphered Text:")
        print("In ASCII: ",util.matrix_list_to_string(cipher_blocks))
        print("In HEX: ",util.block_to_hex_pairs(cipher_blocks))

        print("")
        print("Execution Time in Details:")
        print("Key Schedule Time: ",abs(round((start_time_key-end_time_key)*1000, 4)),"ms")
        print("Encrypton Time: ",abs(round((start_time_encryption-end_time_encryption)*1000, 4)),"ms")
        #-----------------------------------------------

        processed_data = CustomObject(a, b, G, Kapub, (0, 0), p, 77, cipher_blocks)
        server_response = CustomObject(
            a=processed_data.a,
            b=processed_data.b,
            G=processed_data.G,
            Kapub=processed_data.Kapub,
            Kbpub=processed_data.Kbpub,
            p=processed_data.p,
            n=processed_data.n,
            data=processed_data.data  
            )
        #Server Alice sends cipher blocks to Client Bob
        client_socket.send(pickle.dumps(server_response))
        client_socket.close()
        break

if __name__ == "__main__":
    start_server()
