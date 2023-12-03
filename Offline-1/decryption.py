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

message = input("Enter Message to Decrypt: ")
padded_input = util.pad_input(message)
input_chunks = util.chunk_string(padded_input)

user_key =input("Enter a Key: ")
padded_key = util.pad_input(user_key)
key_chunks = util.chunk_string(padded_key)

key = util.string_to_matrix(key_chunks[0])
message = util.string_to_matrix(input_chunks[0])
message = list(map(list, zip(*message)))

message = [
            [0x29, 0x57, 0x40, 0x1a], 
            [0xc3, 0x14, 0x22, 0x02],
            [0x50, 0x20, 0x99, 0xd7],
            [0x5f, 0xf6, 0xb3, 0x3a]
          ]

keys = [[[0] * 4 for _ in range(4)] for _ in range(11)]
keys[0] = key 
for i in range(10):
    print
    key = keyExpand.expand(key, i)
    keys[i+1] = key

print("initial matrix:")
util.print_mat(message)

message = decrypt(message,keys)

print("done")
util.print_mat(message)
message = list(map(list, zip(*message)))
print(util.matrix_to_string(message))
