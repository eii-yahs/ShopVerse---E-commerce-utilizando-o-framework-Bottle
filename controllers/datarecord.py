import json
import os
import time

class JSONDatabase:
    def __init__(self, path):
        self.path = path

    def load(self):
        if os.path.exists(self.path):
            with open(self.path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return data if isinstance(data, list) else []
        return []  

    def save(self, data):
        if not isinstance(data, list):
            raise ValueError("Dados devem ser uma lista!") 
        with open(self.path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

class UserDatabase(JSONDatabase):
    def add_user(self, user):
        users = self.load()
        
        if any(u.get('email') == user.get('email') for u in users):
            raise ValueError("E-mail já cadastrado!")
        
        user.setdefault('login_timestamp', None)
        user.setdefault('foto_perfil', '/static/img/perfil/perfil.png')
        
        users.append(user)
        self.save(users)

    def find_by_email(self, email):
        users = self.load()
        return next((u for u in users if u.get('email') == email), None)
    
    def limpar_timestamps_expirados(self):
        users = self.load()
        for user in users:
            if user.get('login_timestamp') and (time.time() - user['login_timestamp']) > 3600:
                user['login_timestamp'] = None
        self.save(users)

    def update_user(self, email, new_data):
        users = self.load()
        for user in users:
            if user.get('email') == email:
                user.update(new_data)
                self.save(users)
                return True
        return False 


class PendingUserDatabase(JSONDatabase):
    def add_pending_user(self, user):
        pending_users = self.load()
        user['confirmation_timestamp'] = time.time()
        pending_users.append(user)
        self.save(pending_users)
        
    def remover_usuarios_expirados(self):
        pending_users = self.load()
        usuarios_validos = [u for u in pending_users if (time.time() - u['confirmation_timestamp']) <= 300]
        self.save(usuarios_validos)

class ProductDatabase(JSONDatabase):
    def load(self):
        try:
            return super().load()
        except Exception as e:
            print(f"Erro ao carregar produtos: {e}")
            return []

class OrderDatabase(JSONDatabase):
    def __init__(self, file_path):
        super().__init__(file_path)

    def add_order(self, order):
        orders = self.load()
        orders.append(order)
        self.save(orders)

    def get_orders_by_user(self, user_email):
        orders = self.load()
        return [order for order in orders if order["cliente"] == user_email]
