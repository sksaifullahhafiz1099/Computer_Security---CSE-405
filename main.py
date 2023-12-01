from aes import AES

def print_mat(m):
    for row in m:
        for element in row:
            print(hex(element), end=" ")
        print("")
    print("")    

# Creating an instance of the Person class
aes = AES()
matrix = [
    [0x01, 0x0A, 0x1E, 0x3F],
    [0x5B, 0x4D, 0x8C, 0x72],
    [0xA5, 0xE9, 0x2F, 0x6D],
    [0xBF, 0x4A, 0x7C, 0xD8]
]

print("initial matrix:")
print_mat(matrix)

print("substituted matrix:")
m1=aes.substitute_bytes(matrix)
print_mat(m1)

print("shift rows:")
m2=aes.shift_row(m1)
print_mat(m2)

print("mix columns:")
m3=aes.mix_columns(m2)
print_mat(m3)


