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

#-----------------------------------------------------------



def add_points(P, Q, p):
    x1, y1 = P
    x2, y2 = Q
    if x1 == x2 and y1 == y2:
        s = ((3*x1*x2 + a)*pow((2*y1),-1,p))%p
    else:
        s = ((y2 - y1)*pow((x2 - x1),-1,p))%p
    
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
        #print(target_point)
        if current_bit == "1":
            target_point = add_points(target_point, G, p)
    return target_point


#shared----------------------------
p = generate_prime_in_range(100000000000,500000000000)
a = random.randrange(5,p)
G = (random.randrange(3000,4000),random.randrange(5000,6000))
b = G[1]**2 - G[0]**3 - G[0] * a 
lower_limit = p + 1 - 2 * int(p**0.5)
upper_limit = p + 1 + 2 * int(p**0.5)
#----------------------------------

#Alice:
Ka = generate_prime_in_range(2, upper_limit)
Kapub = apply_double_and_add_method(G,Ka,p)
#Bob
Kb = generate_prime_in_range(2, upper_limit)
Kbpub = apply_double_and_add_method(G,Kb,p)
#Alice decrypting:
Key_Alice = apply_double_and_add_method(Kbpub,Ka,p) 
#Bob Decrypting:
Key_Bob = apply_double_and_add_method(Kapub,Kb,p)

print("ans:::")
print(Key_Alice)
print(Key_Bob)
