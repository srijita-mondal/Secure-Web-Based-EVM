import random

p = 467
g = 2

x = random.randint(1, p-2)   # private key
y = pow(g, x, p)             # public key


def encrypt(msg):
    msg_num = sum(ord(c) for c in msg)

    k = random.randint(1, p-2)
    c1 = pow(g, k, p)
    c2 = (msg_num * pow(y, k, p)) % p

    return (c1, c2)


def decrypt(cipher):
    c1, c2 = cipher
    s = pow(c1, x, p)
    s_inv = pow(s, -1, p)
    msg_num = (c2 * s_inv) % p

    return msg_num