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

"""
#taking cipher massage and creating string chunk array
message = input("Enter Message to Decrypt: ")
padded_input = util.pad_input(message)
input_chunks = util.chunk_string(padded_input)
"""

input_chunk_m = [
                    [
                        [0x7f, 0x67, 0xac, 0xf5],
                        [0xc8, 0x6b, 0x44, 0x5b],
                        [0xbe, 0x9d, 0x81, 0xc5],
                        [0x26, 0x20, 0x29, 0x8]
                    ]
                ]

#input_chunk_m = cipher_blocks ----------------------------------cipher blocks will be received

#taking key and creating chunk array(only first one will be used)
user_key =input("Enter a Key: ")
padded_key = util.pad_input(user_key)
key_chunks = util.chunk_string(padded_key)

key = util.string_to_matrix(key_chunks[0])

keys = [[[0] * 4 for _ in range(4)] for _ in range(11)]
keys[0] = key 
for i in range(10):
    print
    key = keyExpand.expand(key, i)
    keys[i+1] = key

"""
encrypted_message = [[0x29, 0xc3, 0x50, 0x5f],
    [0x57, 0x14, 0x20, 0xf6],
    [0x40, 0x22, 0x99, 0xb3],
    [0x1a, 0x2, 0xd7, 0x3a]]
encrypted_message = list(map(list, zip(*encrypted_message)))
encrypted_message = decrypt(encrypted_message, keys)
encrypted_message = list(map(list, zip(*encrypted_message)))
print(util.matrix_to_string(encrypted_message))
"""



plain_blocks = [[[0] * 4 for _ in range(4)] for _ in range(len(input_chunk_m))]
#print(plain_blocks)
#print(input_chunk_m[0])
#print(util.matrix_to_string(input_chunk_m[0]))
for i in range(len(input_chunk_m)):
    print(i)
    P = input_chunk_m[i]
    P = list(map(list, zip(*P)))
    #util.print_mat(P)
    if i == 0:
        plain_blocks[0] = util.xor(decrypt(P,keys),IV)
        plain_blocks[0] = list(map(list, zip(*plain_blocks[0])))
        #print(util.matrix_to_string(plain_blocks[0]))
    else:
        #temp_mat = list(map(list, zip(*input_chunk_m[i-1])))
        temp_mat = input_chunk_m[i-1]
        plain_blocks[i] = util.xor(decrypt(P,keys),temp_mat)
        plain_blocks[i] = list(map(list, zip(*plain_blocks[i])))

#print(util.matrix_to_string(plain_blocks[0]))
#util.print_mat(plain_blocks[0])
#print(plain_blocks)
plain_string = util.matrix_list_to_string(plain_blocks)
print(plain_string)
print("done")
#util.print_mat(message)
#message = list(map(list, zip(*message)))
#print(util.matrix_to_string(message))
