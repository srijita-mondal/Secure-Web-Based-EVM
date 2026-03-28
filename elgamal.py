import random

p = 30803
g = 2
x = 12345  
y = pow(g, x, p)  


def encrypt_vote(m: int):
    k = random.randint(2, p - 2)
    c1 = pow(g, k, p)
    c2 = (m * pow(y, k, p)) % p
    return (c1, c2)


def decrypt_vote(cipher):
    c1, c2 = cipher
    s = pow(c1, x, p)
    s_inv = pow(s, -1, p)
    return (c2 * s_inv) % p