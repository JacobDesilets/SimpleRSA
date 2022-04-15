import argparse
from pathlib import Path

def rsa_decrypt(ciphertext, keys):
    n = keys['n']
    d = keys['d']
    plaintext = ''
    for char in ciphertext:
        decrypted_char = pow(int(char), int(d), int(n))
        plaintext += chr(decrypted_char)
    return plaintext


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="RSA Encryption.")
    parser.add_argument('src', help='Source encrypted text file')
    parser.add_argument('dest', help='Destination text file for decrypted text')
    parser.add_argument('pub_keys', help='Source text file for public keys')
    parser.add_argument('sec_keys', help='Source text file for secret keys')
    args = parser.parse_args()

    src = Path(__file__).with_name(args.src)
    dest = Path(__file__).with_name(args.dest)
    pub_keys = Path(__file__).with_name(args.pub_keys)
    sec_keys = Path(__file__).with_name(args.sec_keys)

    keys = {}

    src_f = open(src)
    ciphertext = src_f.readlines()
    src_f.close()
    
    pub_keys_f = open(pub_keys)
    pkl = pub_keys_f.readlines()
    keys['n'] = pkl[0]
    keys['e'] = pkl[1]
    pub_keys_f.close()

    sec_keys_f = open(sec_keys)
    skl = sec_keys_f.readlines()
    keys['p'] = skl[0]
    keys['q'] = skl[1]
    keys['phi'] = skl[2]
    keys['d'] = skl[3]
    sec_keys_f.close()

    plaintext = rsa_decrypt(ciphertext, keys)

    dest_f = open(dest, 'w')
    dest_f.write(plaintext)
    dest_f.close()

