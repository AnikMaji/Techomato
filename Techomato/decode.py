import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet



class Decode:

    def funcDecode(self, string):
        from .password import password
        pwd=password()
        password_provided = pwd.pwd
        password = password_provided.encode()
        salt = b'salt_'
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))

        encrypted = string
        f = Fernet(key)
        decrypted = f.decrypt(encrypted)
        return(str(decrypted)[2:-1])