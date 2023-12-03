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

message = input("Enter something: ")
padded_input = util.pad_input(message)
input_chunks = util.chunk_string(padded_input)

user_key =input("Enter a Key: ")
padded_key = util.pad_input(user_key)
key_chunks = util.chunk_string(padded_key)

key = util.string_to_matrix(key_chunks[0])
message = util.string_to_matrix(input_chunks[0])
message = list(map(list, zip(*message)))

"""
for element in input_chunks:
    util.print_mat(util.string_to_matrix(element))
"""
print("initial matrix:")
util.print_mat(message)

message = encrypt(message,key)

util.print_mat(message)
print(util.matrix_to_string(message))
print("complete")