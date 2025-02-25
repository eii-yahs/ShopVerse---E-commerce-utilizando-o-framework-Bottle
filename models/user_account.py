import os

class UserAccount:
    def __init__(self, nome, data_nascimento, telefone, email, senha, foto_perfil="/static/img/perfil/default.png", login_timestamp=None, carrinho = None, recovery_token=None):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.telefone = telefone
        self.email = email
        self.senha = senha
        self.foto_perfil = foto_perfil
        self.login_timestamp = login_timestamp
        self.carrinho = carrinho if carrinho is not None else {}
        self.recovery_token = recovery_token

    
    def update_profile_image(self, image_path):
        if os.path.exists(image_path):
            self.foto_perfil = image_path
        else:
            raise FileNotFoundError("Imagem não encontrada.")
    
    def to_dict(self):
        return {
            "nome": self.nome,
            "data_nascimento": self.data_nascimento,
            "telefone": self.telefone,
            "email": self.email,
            "senha": self.senha,
            "foto_perfil": self.foto_perfil,
            "login_timestamp": self.login_timestamp,
            "carrinho": self.carrinho,
            "recovery_token": self.recovery_token
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            nome=data["nome"],
            data_nascimento=data["data_nascimento"],
            telefone=data["telefone"],
            email=data["email"],
            senha=data["senha"],
            foto_perfil=data.get("foto_perfil", "/static/img/perfil/default.png"),
            login_timestamp=data.get("login_timestamp"),
            carrinho=data.get("carrinho", {}),
            recovery_token=data.get("recovery_token")
        )