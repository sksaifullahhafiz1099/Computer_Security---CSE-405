from aes import AES
from key import Key
import time
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
start_time_key = time.time()
padded_key = util.pad_input(user_key)
key_chunks = util.chunk_string(padded_key)

#only the first chunk is taken as the key matrix
key = util.string_to_matrix(key_chunks[0])
end_time_key = time.time()

print("")
print("key:")
print("In ASCII: ",key_chunks[0])
print("In HEX: ",util.string_to_hex_pairs(key_chunks[0]))
print("")
print("Plain Text:")
print("In ASCII: ",message)
print("In HEX: ",util.string_to_hex_pairs(message))
#-----------------------------------------------

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


input_chunk_m = cipher_blocks
print("")
print("Ciphered Text:")
print("In ASCII: ",util.matrix_list_to_string(cipher_blocks))
print("In HEX: ",util.block_to_hex_pairs(cipher_blocks))

#user_key =input("Enter a Key: ")
#padded_key = util.pad_input(user_key)
#key_chunks = util.chunk_string(padded_key)

#key = util.string_to_matrix(key_chunks[0])

keys = [[[0] * 4 for _ in range(4)] for _ in range(11)]
keys[0] = key 
for i in range(10):
    print
    key = keyExpand.expand(key, i)
    keys[i+1] = key

plain_blocks = [[[0] * 4 for _ in range(4)] for _ in range(len(input_chunk_m))]

start_time_decryption = time.time()
for i in range(len(input_chunk_m)):
    P = input_chunk_m[i]
    P = list(map(list, zip(*P)))
    if i == 0:
        plain_blocks[0] = util.xor(decrypt(P,keys),IV)
        plain_blocks[0] = list(map(list, zip(*plain_blocks[0])))
    else:
        #temp_mat = list(map(list, zip(*input_chunk_m[i-1])))
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
print("Key Schedule Time: ",abs(round((start_time_key-end_time_key)*1000, 4)),"ms")
print("Encrypton Time: ",abs(round((start_time_encryption-end_time_encryption)*1000, 4)),"ms")
print("Decryption Time: ",abs(round((start_time_decryption-end_time_decryption)*1000, 4)),"ms")

