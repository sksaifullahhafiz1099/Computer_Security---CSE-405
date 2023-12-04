import random
from sympy import isprime

def is_prime(n, k=5):
    if n <= 1:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False

    # Write n as 2^r * d + 1
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    # Witness loop
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False  # n is composite

    return True  # n is probably prime

def generate_prime_in_range(lower, upper):
    n = random.randint(lower, upper)
    while not is_prime(n):
        n = random.randint(lower, upper)
    return n



sets = [
[1049,1628, 3704],
[5087,2192, 5909],
[5987,5250, 3183],
[8999,2026, 4728],
[4951,2575, 699]
]

#-----------------------------------------------------------

def add_points(P, Q, p):
    x1, y1 = P
    x2, y2 = Q
    if x1 == x2 and y1 == y2:
        s = (3*x1*x2 + a) /(2*y1)
    else:
        s = (y2 - y1)/(x2 - x1)
    x3 = (s*s - x1 - x2) % p
    y3 = (s * (x1 - x3) - y1) % p        
    return x3, y3
 
     
def apply_double_and_add_method(G, k, p):
    target_point = G
    k_binary = bin(k)[2:] #0b1111111001
    for i in range(1, len(k_binary)):
        current_bit = k_binary[i: i+1]
        # doubling - always
        target_point = add_points(target_point, target_point, p)
        if current_bit == "1":
            target_point = add_points(target_point, G, p)
    return target_point

#shared----------------------------
a = 2
b = 3  
index = random.randint(0, 4)
print(index)
p = sets[index][0]
G = (sets[index][1],sets[index][2])

lower_limit = p + 1 - 2 * int(p**0.5)
upper_limit = p + 1 + 2 * int(p**0.5)
#----------------------------------

#Alice:
Ka = generate_prime_in_range(lower_limit, upper_limit)
print(Ka)
Kapub = apply_double_and_add_method(G,Ka,p)
print(Kapub)
#Bob
Kb = generate_prime_in_range(lower_limit, upper_limit)
print(Kb)
Kbpub = apply_double_and_add_method(G,Kb,p)
print(Kbpub)
#Alice decrypting:
Key_Alice = apply_double_and_add_method(Kbpub,Ka,p) 
#Bob Decrypting:
Key_Bob = apply_double_and_add_method(Kapub,Kb,p)

print(Key_Alice)
print(Key_Bob)


