class Util:
    def __init__(self) -> None:
        pass
    
    def print_mat_row(self,m):
        for row in m:
            for element in row:
                print(hex(element), end=" ")
        print("") 

    def print_mat(self,m):
        for row in m:
            for element in row:
                print(hex(element), end=" ")
            print("")
        print("")    

    def pad_input(self,input_str):
        remaining_bits = len(input_str) % 16
        padding_bits = 0
        if remaining_bits > 0 :
            padding_bits = 16 - remaining_bits
        padded_input = input_str + ' ' * padding_bits
        return padded_input

    def chunk_string(self,input_str):
        input_array = [input_str[i:i + 16] for i in range(0, len(input_str), 16)]
        return input_array

    def string_to_matrix(self,input_str):
        if len(input_str) != 16:
            raise ValueError("Input string must be 16 characters long.")
        hex_values = [ord(char) for char in input_str]
        matrix = [[hex_values[i + j * 4] for i in range(4)] for j in range(4)]
        return matrix
    
    def matrix_to_string(self,matrix):
        result_string = ""
        for row in matrix:
            for element in row:
                result_string += chr(element)
        return result_string
    
    def matrix_list_to_string(self,matrix):
        result_string = ""
        for i in range(len(matrix)):
            for row in matrix[i]:
                for element in row:
                    result_string += chr(element)
        return result_string
    
    def matrix_list_to_string_inv(self,matrix):
        result_string = ""
        for i in range(len(matrix)):
            matrix[i] = list(map(list, zip(*matrix[i])))
            for row in matrix[i]:
                for element in row:
                    result_string += chr(element)
        return result_string

    def xor(self,a,b):
        x = [[0] * 4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                x[i][j] = a[i][j]^b[i][j]
        return x
    
    def string_to_hex_pairs(self,input_string):
        hex_pairs = ""
        for char in input_string:
            hex_value = hex(ord(char))[2:]  # Convert ASCII to hex and remove the '0x' prefix
            hex_pairs += str(hex_value) + " "

        return hex_pairs
    
    def block_to_hex_pairs(self,matrix):
        hex_pairs = ""
        for i in range(len(matrix)):
            for row in matrix[i]:
                for element in row:
                    hex_value = hex(element)[2:]
                    hex_pairs += str(hex_value) + " "

        return hex_pairs