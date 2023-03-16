import os
import hashlib

def generate_key(password : str):
    # random salt
    salt = os.urandom(32)
    # hash the password
    hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    # return the salt and hash(together)
    return (salt + hash).hex()

def check_password(password : str, key: str):
    # Getting the salt and hash from the key
    salt = bytearray.fromhex(key[:64])  # 32 is the length of the salt
    hash = key[64:]                     # 32 is the length of the hash
    
    # generating a new hash
    new_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt, 
        100000
    ).hex()

    if new_hash == hash:
        return True
    else:
        return False
