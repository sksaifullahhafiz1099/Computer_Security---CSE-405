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
user_key =input("Enter a Key: ")
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


#--- cipher block is the sending data