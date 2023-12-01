from aes import AES

from util import Util

hex_matrix = [
    [0x01, 0x02, 0x03, 0x04],
    [0x05, 0x06, 0x07, 0x08],
    [0x09, 0x0A, 0x0B, 0x0C],
    [0x0D, 0x0E, 0x0F, 0x10]
]

util = Util()
aes = AES()

message = input("Enter something: ")
padded_input = util.pad_input(message)
input_chunks = util.chunk_string(padded_input)

user_key =input("Enter a Key: ")
padded_key = util.pad_input(user_key)
key_chunks = util.chunk_string(padded_key)
key = util.string_to_matrix(key_chunks[0])

for element in input_chunks:
    util.print_mat(util.string_to_matrix(element))

print("initial matrix:")
util.print_mat(util.string_to_matrix(input_chunks[0]))

print("substituted matrix:")
m1=aes.substitute_bytes(util.string_to_matrix(input_chunks[0]))
util.print_mat(m1)

print("shift rows:")
m2=aes.shift_row(m1)
util.print_mat(m2)

print("mix columns:")
m3=aes.mix_columns(m2)
util.print_mat(m3)


print("round key:")
m4=aes.add_round_key(m3,key)
util.print_mat(m4)