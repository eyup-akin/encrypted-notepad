from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os
import json
from utils import get_path  # Utils'ten yolu alıyoruz


class SecurityManager:
    def __init__(self, password):
        self.password = password.encode()

    def derive_key(self, salt):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.password))
        return key

    def encrypt_and_save(self, data, filename):
        full_path = get_path(filename)
        salt = os.urandom(16)
        key = self.derive_key(salt)
        cipher = Fernet(key)

        json_data = json.dumps(data)
        encrypted_data = cipher.encrypt(json_data.encode())

        with open(full_path, "wb") as f:
            f.write(salt + encrypted_data)

    def load_and_decrypt(self, filename):
        full_path = get_path(filename)
        if not os.path.exists(full_path):
            return {}

        with open(full_path, "rb") as f:
            file_content = f.read()

        salt = file_content[:16]
        encrypted_data = file_content[16:]

        key = self.derive_key(salt)
        cipher = Fernet(key)

        try:
            decrypted_data = cipher.decrypt(encrypted_data).decode()
            return json.loads(decrypted_data)
        except Exception:
            raise ValueError("Şifre çözülemedi!")