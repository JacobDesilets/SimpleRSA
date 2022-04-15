import argparse, random
from pathlib import Path

# GLOBALS
MILLER_RABIN_LIMIT = 10
BIT = 128


def n_bit_random(n):
    return random.randrange(2 ** (n - 1) + 1, 2 ** n - 1)


def is_prime(n):
    for i in range(0, MILLER_RABIN_LIMIT):
        a = random.randint(1, n-1)
        if pow(a, n-1, n) != 1:  # a^(n-1) (mod n)
            return False
    return True


def gcd(x, y):
    while y:
        x, y = y, x % y
    return x


def are_coprime(x, y):
    return gcd(x, y) == 1


def random_prime():
    while True:
        n = n_bit_random(BIT)
        if is_prime(n):
            return n


def calc_e(phi):
    for i in range(3, phi):
        if i % 2 != 0 and are_coprime(i, phi):
            return i


def generate_keys():
    keys = {}
    p = random_prime()
    q = random_prime()
    n = p * q
    phi = (p - 1) * (q - 1)
    e = calc_e(phi)
    d = pow(e, -1, phi)

    keys['p'] = n
    keys['q'] = q
    keys['n'] = n
    keys['phi'] = phi
    keys['e'] = e
    keys['d'] = d

    return keys


def encrypt(plaintext, keys):
    ciphertext = ''
    n = keys['n']
    e = keys['e']
    for char in plaintext:
        m = ord(char)
        encrypted_char = pow(m, e, n)
        ciphertext += f'{encrypted_char}\n'
    return ciphertext



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="RSA Encryption.")
    parser.add_argument('src', help='Source text file')
    parser.add_argument('dest', help='Destination text file for encrypted text')
    parser.add_argument('pub_keys', help='Destination text file for public keys')
    parser.add_argument('sec_keys', help='Destination text file for secret keys')
    args = parser.parse_args()

    src = Path(__file__).with_name(args.src)
    dest = Path(__file__).with_name(args.dest)
    pub_keys = Path(__file__).with_name(args.pub_keys)
    sec_keys = Path(__file__).with_name(args.sec_keys)

    src_f = open(src)
    plaintext = src_f.read()
    src_f.close()

    keys = generate_keys()

    ciphertext = encrypt(plaintext, keys)
    
    dest_f = open(dest, 'w')
    dest_f.write(ciphertext)
    dest_f.close()

    pub_keys_f = open(pub_keys, 'w')
    pub_keys_f.write(f'{keys["n"]}\n{keys["e"]}')
    pub_keys_f.close()

    sec_keys_f = open(sec_keys, 'w')
    sec_keys_f.write(f'{keys["p"]}\n{keys["q"]}\n{keys["phi"]}\n{keys["d"]}')
    sec_keys_f.close()
