import socket
import pickle
import time
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

    # Step 1: Client receives public variables and Kapub from the server Alice
    server_data = client_socket.recv(1024)
    server_object = pickle.loads(server_data)

    #Bob generates kbpub using public variables and kapub
    
    upper_limit = server_object.p + 1 + 2 * int(server_object.p**0.5)
    Kb = generate_prime_in_range(2, upper_limit)
    Kbpub = apply_double_and_add_method(server_object.G, Kb, server_object.p, server_object.a)
    key_bob = apply_double_and_add_method(server_object.Kapub, Kb, server_object.p, server_object.a)
    print("Bob's key int: ",key_bob[0])

    client_data = CustomObject(
        a=server_object.a,
        b=server_object.b,
        G=server_object.G,
        Kapub=server_object.Kapub,
        Kbpub=Kbpub,
        p=server_object.p,
        n=1, 
        data=[[[]]] 
    )
    
    # Step 2: Client Bob sends Kbpub to server Alice
    client_socket.send(pickle.dumps(client_data))

    # Step 3: Client Bob receives the cipher blocks from the server Alicse
    server_response_data = client_socket.recv(1024)
    server_response_object = pickle.loads(server_response_data)
    

    #AES decryption process with CBC
    #----------------------------------------------------
    from aes import AES
    from key import Key
    from util import Util

    def decrypt(message,keys):
        for i in range(11):
            if i == 0:
                message = aes.add_round_key(message,keys[10-i]) 
            if i <= 9 and i > 0:
                message = aes.inv_shift_row(message)
                message = aes.inv_substitute_bytes(message)
                message = aes.add_round_key(message,keys[10-i])
                message = aes.inv_mix_columns(message)  
            if i == 10:
                message = aes.inv_shift_row(message)
                message = aes.inv_substitute_bytes(message) 
                message = aes.add_round_key(message,keys[10-i])
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
    
    cipher_blocks = server_response_object.data
    input_chunk_m = cipher_blocks

    #accessing key made using elliptic curve cryptography
    hex_values = [hex(ord(char))[2:] for char in str(key_bob[0])]
    hex_string = ''.join(hex_value.zfill(2) for hex_value in hex_values)
    user_key = hex_string
    padded_key = util.pad_input(user_key)
    key_chunks = util.chunk_string(padded_key)

    key = util.string_to_matrix(key_chunks[0])
    #print("key: ",key_chunks[0])
    print("")
    print("key:")
    print("In ASCII: ",key_chunks[0])
    print("In HEX: ",util.string_to_hex_pairs(key_chunks[0]))

    #making key for 11 steps of AES decryption
    keys = [[[0] * 4 for _ in range(4)] for _ in range(11)]
    keys[0] = key 
    for i in range(10):
        key = keyExpand.expand(key, i)
        keys[i+1] = key

    plain_blocks = [[[0] * 4 for _ in range(4)] for _ in range(len(input_chunk_m))]

    #AES_decryption-----------------------------------
    start_time_decryption = time.time()
    for i in range(len(input_chunk_m)):
        P = input_chunk_m[i]
        P = list(map(list, zip(*P)))
        if i == 0:
            plain_blocks[0] = util.xor(decrypt(P,keys),IV)
            plain_blocks[0] = list(map(list, zip(*plain_blocks[0])))
        else:
            temp_mat = input_chunk_m[i-1]
            plain_blocks[i] = util.xor(decrypt(P,keys),temp_mat)
            plain_blocks[i] = list(map(list, zip(*plain_blocks[i])))
    end_time_decryption = time.time()
    plain_string = util.matrix_list_to_string(plain_blocks)
    print("")
    print("Deciphered Text:")
    print("In ASCII: ",plain_string)
    print("In HEX: ",util.string_to_hex_pairs(plain_string))

    print("")
    print("Execution Time in Details:")
    print("Decryption Time: ",abs(round((start_time_decryption-end_time_decryption)*1000, 4)),"ms")
    #----------------------------------------------------

    client_socket.close()

if __name__ == "__main__":
    start_client()
