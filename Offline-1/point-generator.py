import random
from sympy import isprime

def generate_random_prime(min_value=10**3):
    while True:
        candidate = random.randint(min_value, min_value * 10)
        if isprime(candidate):
            return candidate

# Example usage
random_prime = generate_random_prime()
print("Random Prime Number:", random_prime)

import random

def is_quadratic_residue(x, p):
    return pow(x, (p - 1) // 2, p) == 1

def find_square_root_mod_p(a, p):
    if not is_quadratic_residue(a, p):
        return None  # No square root exists
    else:
        # Using Euler's criterion and Tonelli-Shanks algorithm
        q, s = p - 1, 0
        while q % 2 == 0:
            q //= 2
            s += 1
        
        # Find a non-residue modulo p
        n = 2
        while is_quadratic_residue(n, p):
            n += 1

        z = pow(n, q, p)
        c = pow(n, (q + 1) // 2, p)
        t = pow(a, q, p)
        r = pow(a, (q + 1) // 2, p)

        while True:
            if t == 0:
                return 0
            elif t == 1:
                return r
            else:
                i, tt = 0, t
                while tt != 1:
                    tt = (tt * tt) % p
                    i += 1

                b = pow(c, 2 ** (s - i - 1), p)
                s, c, t, r = i, (b * b) % p, (t * b * b) % p, (r * b) % p

def generate_point_on_curve(a, b, p):
    while True:
        x = random.randint(1, p - 1)
        y_sq = (x**3 + a*x + b) % p
        y = find_square_root_mod_p(y_sq, p)
        if y is not None:
            return (x, y)

p = generate_random_prime() 
a = 2  
b = 3   

random_point = generate_point_on_curve(a, b, p)
print("Generated Point:", random_point)