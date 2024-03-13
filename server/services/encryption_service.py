import os

from cryptography.fernet import Fernet

class EncryptionService:
    def __init__(self):
        key= os.getenv('ENCRYPT_KEY', '')
        self.cipher_suite = Fernet(key)

    def encrypt(self, data):
        data_bytes = data.encode()
        return self.cipher_suite.encrypt(data_bytes)

    def decrypt(self, data):
        return self.cipher_suite.decrypt(data).decode()