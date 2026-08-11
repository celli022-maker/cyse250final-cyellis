"""
Fernet-based convenience wrappers for symmetric encryption.
- gen_key() -> bytes
- encrypt_message(key, plaintext) -> token (bytes)
- decrypt_message(key, token) -> plaintext (str)
"""

from cryptography.fernet import Fernet

def gen_key() -> bytes:
    return Fernet.generate_key()

def encrypt_message(key: bytes, plaintext: str) -> bytes:
    f = Fernet(key)
    return f.encrypt(plaintext.encode('utf-8'))

def decrypt_message(key: bytes, token: bytes) -> str:
    f = Fernet(key)
    return f.decrypt(token).decode('utf-8')