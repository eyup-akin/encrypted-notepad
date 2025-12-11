import json
import os
import hashlib
from utils import get_path


class UserManager:
    def __init__(self, db_file="users.json"):
        self.db_file = get_path(db_file)
        self.users = self.load_users()

    def load_users(self):
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}

    def save_users(self):
        with open(self.db_file, "w") as f:
            json.dump(self.users, f)

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, username, password):
        if username in self.users:
            return False, "Bu kullanıcı adı zaten var!"

        self.users[username] = {
            "password_hash": self.hash_password(password)
        }
        self.save_users()
        return True, "Kayıt başarılı! Şimdi giriş yapabilirsiniz."

    def login_user(self, username, password):
        if username not in self.users:
            return False, "Kullanıcı bulunamadı!"

        stored_hash = self.users[username]["password_hash"]
        if stored_hash == self.hash_password(password):
            return True, "Giriş Başarılı"
        else:
            return False, "Parola hatalı!"

    def delete_user(self, username):
        if username in self.users:
            del self.users[username]
            self.save_users()
            user_file = get_path(f"notlar_{username}.bin")
            if os.path.exists(user_file):
                os.remove(user_file)
            return True, "Hesap ve tüm veriler silindi."
        return False, "Kullanıcı bulunamadı."


    def get_all_usernames(self):
        """Kayıtlı kullanıcı adlarının listesini döndürür."""
        return list(self.users.keys())