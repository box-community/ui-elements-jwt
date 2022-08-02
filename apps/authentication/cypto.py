from cryptography.fernet import Fernet
from apps.config import Config

def encrypt_token(token:str) -> str:
    key = Config.FERNET_KEY
    encoded_token = token.encode()
    f = Fernet(key)
    encrypted = f.encrypt(encoded_token)
    return encrypted.decode()

def decrypt_token(token:str) -> str:
    key = Config.FERNET_KEY
    encoded_token = token.encode()
    f = Fernet(key)
    dencrypted = f.decrypt(encoded_token)
    return dencrypted.decode()