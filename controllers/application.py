from .email_service import EmailService
from bottle import template, redirect, request, response
import json
import uuid
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import time
import re
import random
from .email_service import EmailService
from .variables import UPLOAD_FOLDER, ALLOWED_EXTENSIONS, user_db, product_db, pending_db, order_db

from models.user_account import UserAccount 

class Application:
    def __init__(self, sio=None):
        # Rotas GET
        self.pages = {
            'index': self.index,
            'login': self.login_page,
            'cadastro': self.cadastro_page,
            'verificacao': self.verificacao_page,
            'editar_perfil': self.editar_perfil,
            'senha': self.verificacao_form,
            'recuperar_senha': self.recuperar_senha,
            'novasenha': self.novasenha,
            'macbooks': self.macbooks,
            'iphone': self.iphone,
            'pcsamsung': self.pcsamsung,
            'celsamsung': self.celsamsung,
            'perfil': self.perfil,
            'produto': self.produto,
            'carrinho': self.visualizar_carrinho,
            'check_login': self.check_login,
            'logout': self.logout
        }

        # Rotas POST
        self.post_routes = {
            'adicionar_ao_carrinho': self.adicionar_ao_carrinho,
            'remover_do_carrinho': self.remover_do_carrinho,
            'login': self.login,
            'cadastro': self.cadastro,
            'verificacao': self.verificacao,
            'finalizar_compra': self.finalizar_compra
        }

        self.user_db = user_db
        self.product_db = product_db
        self.pending_db = pending_db
        self.order_db = order_db
        self.email_service = EmailService()
        self.sio = sio
        
    def render(self, page, parameter=None, is_post=False):
        if is_post:
            handler = self.post_routes.get(page)
            return handler() if handler else {"status": "erro", "mensagem": "Rota POST não encontrada"}
        else:
            handler = self.pages.get(page, self.index)
            return handler(parameter) if parameter else handler()
        
    def get_session_id(self):
        return request.get_cookie('user', secret='chave_secreta')
    
    def validar_senha(self, senha):
        if len(senha) < 8:
            return False
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', senha):
            return False
        if not re.search(r'[A-Z]', senha):
            return False
        if not re.search(r'[0-9]', senha):
            return False
        
        return True
    
    def index(self):
        produtos = self.product_db.load()
        categorias = {}
        for produto in produtos:
            categoria = produto["categoria"]
            if categoria not in categorias:
                categorias[categoria] = []
            categorias[categoria].append(produto)

        user = None
        user_email = self.get_session_id() 
        
        if user_email:
            user_data = self.user_db.find_by_email(user_email)
            if user_data:
                user = UserAccount.from_dict(user_data)
        
        return template('html/index', categorias=categorias, user=user.to_dict() if user else {})
    
    def login_page(self):
        return template('html/autenticacao/login')
    
    def cadastro_page(self):
        return template('html/autenticacao/cadastro')
    
    def verificacao_page(self):
        return template('html/autenticacao/verificacao')
    
    def editar_perfil(self):
        user_email = self.get_session_id()  
        if not user_email:
            return redirect('/login')
        
        users = [UserAccount.from_dict(u) for u in self.user_db.load()]
        
        user_index = next((i for i, u in enumerate(users) if u.email == user_email), None)
        
        if user_index is None:
            return redirect('/perfil')
        
        user = users[user_index]

        if request.method == 'POST':
            user.nome = request.forms.get("nome", user.nome)
            user.telefone = request.forms.get("telefone", user.telefone)
            user.data_nascimento = request.forms.get("data_nascimento", user.data_nascimento)

            if request.forms.get("remover_foto") == "1":
                user.foto_perfil = '/static/img/perfil/perfil.png'
            else:
                foto_perfil = request.files.get('foto_perfil')
                if foto_perfil and self.allowed_file(foto_perfil.filename):
                    filename = secure_filename(foto_perfil.filename)
                    unique_filename = f"{uuid.uuid4()}.{filename.split('.')[-1]}"
                    file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
                    
                    foto_perfil.save(file_path)
                    user.foto_perfil = f'/{os.path.join(UPLOAD_FOLDER, unique_filename)}'

            users[user_index] = user
            self.user_db.save([u.to_dict() for u in users])
            
            return redirect('/perfil')

        return template('html/editar', user=user.to_dict())

    
    def verificacao_form(self):
        return template('html/autenticacao/senha')
    
    def recuperar_senha(self):
        data = request.json
        if not data or 'email' not in data:
            response.status = 400
            return json.dumps({"status": "erro", "message": "E-mail não fornecido."})

        email = data['email']
        users = [UserAccount.from_dict(u) for u in self.user_db.load()]

        for user in users:
            if user.email == email:
                user.recovery_token = str(uuid.uuid4())
                user_db.save([u.to_dict() for u in users])
                
                corpo_email = f"""
                Olá, {user.nome},

                Recebemos uma solicitação para a recuperação de sua senha no ShopVerse. Para redefinir sua senha, clique no link abaixo:

                Link de recuperação: http://127.0.0.1:5000/novasenha/{user.recovery_token}

                Caso não tenha solicitado a recuperação de senha, ignore este e-mail.

                Atenciosamente,
                Equipe ShopVerse
                """

                if EmailService.send_email(email, "Recuperação de Senha - ShopVerse", corpo_email):
                    return json.dumps({"status": "sucesso", "message": "E-mail de recuperação enviado!"})
                return json.dumps({"status": "erro", "message": "Erro ao enviar e-mail."})
        
        response.status = 404
        return {"status": "erro", "message": "E-mail não encontrado."}
    
    def novasenha(self, token):
        users = [UserAccount.from_dict(u) for u in user_db.load()]
        user = next((u for u in users if u.recovery_token == token), None)

        if request.method == 'POST':
            data = request.json
            nova_senha = data.get('nova_senha')
            
            if not self.validar_senha(nova_senha):
                return {"status": "erro", "mensagem": "A senha deve ter pelo menos 8 caracteres, cumprindo os requisitos pedidos."}
            
            if user and nova_senha:
                user.senha = nova_senha
                user.recovery_token = None
                
                user_db.save([u.to_dict() for u in users])
                return json.dumps({"status": "sucesso", "message": "Senha atualizada!"})
            
            return json.dumps({"status": "erro", "message": "Link inválido ou senha ausente."})

        return template('html/autenticacao/novasenha', token=token)
    
    def macbooks(self):
        produtos = [p for p in product_db.load() if p['categoria'] == 'MacBook']
        user_email = self.get_session_id()  
        user = None
        
        if user_email:
            user_data = self.user_db.find_by_email(user_email)
            if user_data:
                user = UserAccount.from_dict(user_data).to_dict()

        return template('html/produtos/macbooks', produtos=produtos, user=user or {})
    
    def iphone(self):
        produtos = [p for p in product_db.load() if p['categoria'] == 'iPhone']
        user_email = self.get_session_id()  
        user = None
        
        if user_email:
            user_data = self.user_db.find_by_email(user_email)
            if user_data:
                user = UserAccount.from_dict(user_data).to_dict()

        return template('html/produtos/iphone', produtos=produtos, user=user or {})
    
    def pcsamsung(self):
        produtos = [p for p in product_db.load() if p['categoria'] == 'Computador Samsung']
        user_email = self.get_session_id()  
        user = None
        
        if user_email:
            user_data = self.user_db.find_by_email(user_email)
            if user_data:
                user = UserAccount.from_dict(user_data).to_dict()

        return template('html/produtos/pcsamsung', produtos=produtos, user=user or {})
    
    def celsamsung(self):
        produtos = [p for p in product_db.load() if p['categoria'] == 'Celular Samsung']
        user_email = self.get_session_id()  
        user = None
        
        if user_email:
            user_data = self.user_db.find_by_email(user_email)
            if user_data:
                user = UserAccount.from_dict(user_data).to_dict()

        return template('html/produtos/celsamsung', produtos=produtos, user=user or {})
    
    def perfil(self):
        user_email = self.get_session_id()  
        users = [UserAccount.from_dict(u) for u in user_db.load()]
        user = next((u for u in users if u.email == user_email), None)
        
        if not user:
            return redirect('/')
        
        return template('html/perfil', user=user.to_dict(), logged_in=True)
    
    def produto(self, id):
        produtos = product_db.load()
        produto = next((p for p in produtos if str(p['id']) == id), None)

        if not produto:
            return redirect('/')

        user_email = self.get_session_id()  
        users = user_db.load()
        user = next((u for u in users if u['email'] == user_email), None)

        return template('html/produtos/produto', produto=produto, user=user or {})
    
    def visualizar_carrinho(self):
        user_email = self.get_session_id()  
        if not user_email:
            return redirect('/login')

        users = [UserAccount.from_dict(u) for u in self.user_db.load()]
        user = next((u for u in users if u.email == user_email), None)
        
        if not user:
            return redirect('/login')
        
        produtos = self.product_db.load()
        
        itens_carrinho = []
        total = 0
        
        for produto in produtos:
            produto_id = str(produto['id'])
            if produto_id in user.carrinho:
                produto_completo = produto.copy()
                produto_completo['quantidade'] = user.carrinho[produto_id]
                produto_completo['subtotal'] = produto_completo['preco'] * produto_completo['quantidade']
                itens_carrinho.append(produto_completo)
                total += produto_completo['subtotal']

        return template(
            'html/carrinho', 
            produtos=itens_carrinho, 
            total=total, 
            user=user.to_dict()
        )
        
    def adicionar_ao_carrinho(self):
        user_email = self.get_session_id()
        if not user_email:
            response.status = 401
            return {"status": "erro", "mensagem": "Login necessário!"}

        users = self.user_db.load()
        user_index = next((i for i, u in enumerate(users) if u['email'] == user_email), None)
        
        if user_index is None:
            return {"status": "erro", "mensagem": "Usuário não encontrado!"}
        
        user = UserAccount.from_dict(users[user_index])
        produto_id = request.forms.get('produto_id')
        quantidade = int(request.forms.get('quantidade', 1))

        produtos = self.product_db.load()
        produto = next((p for p in produtos if str(p['id']) == produto_id), None)

        if not produto:
            return {"status": "erro", "mensagem": "Produto não encontrado!"}

        if produto["estoque"] < quantidade:
            return {"status": "erro", "mensagem": "Estoque insuficiente!"}

        # Atualiza estoque
        produto["estoque"] -= quantidade
        self.product_db.save(produtos)

        # Atualiza carrinho
        if produto_id in user.carrinho:
            user.carrinho[produto_id] += quantidade
        else:
            user.carrinho[produto_id] = quantidade

        users[user_index] = user.to_dict()
        self.user_db.save(users)

        # Socket.IO
        if self.sio:
            self.sio.emit("atualizar_estoque", {"produto_id": produto_id, "estoque": produto["estoque"]})
            self.sio.emit("atualizar_carrinho", {"produto_id": produto_id, "quantidade": user.carrinho[produto_id]})
        
        self.enviar_notificacao(f"{quantidade}x {produto['nome']} adicionado ao carrinho!")
        return {"status": "sucesso", "mensagem": "Produto adicionado ao carrinho!"}

    def remover_do_carrinho(self):
        user_email = self.get_session_id()
        if not user_email:
            return {"status": "erro", "mensagem": "Login necessário!"}

        produto_id = request.forms.get('produto_id')
        users = self.user_db.load()
        user_index = next((i for i, u in enumerate(users) if u['email'] == user_email), None)
        
        if user_index is None:
            return {"status": "erro", "mensagem": "Usuário não encontrado!"}
        
        user = UserAccount.from_dict(users[user_index])
        produtos = self.product_db.load()
        produto = next((p for p in produtos if str(p['id']) == produto_id), None)
        
        if not produto:
            return {"status": "erro", "mensagem": "Produto não encontrado!"}

        if produto_id in user.carrinho:
            quantidade_removida = user.carrinho[produto_id]
            produto["estoque"] += quantidade_removida
            del user.carrinho[produto_id]

            self.product_db.save(produtos)
            users[user_index] = user.to_dict()
            self.user_db.save(users)

            if self.sio:
                self.sio.emit("atualizar_estoque", {"produto_id": produto_id, "estoque": produto["estoque"]})
                self.sio.emit("atualizar_carrinho", {"produto_id": produto_id, "quantidade": 0})

        return {"status": "sucesso", "mensagem": f"{produto['nome']} removido do carrinho!"}

    def login(self):
        data = request.json
        users = [UserAccount.from_dict(u) for u in self.user_db.load()]
        
        for user in users:
            if user.email == data['email'] and user.senha == data['senha']:
                user.login_timestamp = time.time()
                
                if not hasattr(user, 'carrinho'):
                    user.carrinho = {}
                
                self.user_db.save([u.to_dict() for u in users])
                response.set_cookie("user", user.email, secret="chave_secreta", max_age=3600, path="/")
                return {"message": "Login bem-sucedido!"}
        
        response.status = 401
        return {"error": "Credenciais inválidas"}

    def cadastro(self):
        pending_users = self.pending_db.load()
        users = self.user_db.load()
        
        nome = request.forms.get('nome')
        data_nascimento = request.forms.get('data_nascimento')
        telefone = request.forms.get('telefone')
        email = request.forms.get('email')
        senha = request.forms.get('senha')
        
        if not self.validar_senha(senha):
            return {"status": "erro", "mensagem": "A senha deve ter pelo menos 8 caracteres, cumprindo os requisitos pedidos."}
        
        if any(user['email'] == email for user in users + pending_users):
            return {"status": "erro", "mensagem": "E-mail já cadastrado"}
        
        novo_usuario = UserAccount(
            nome=nome,
            data_nascimento=data_nascimento,
            telefone=telefone,
            email=email,
            senha=senha,
            foto_perfil="/static/img/perfil/perfil.png"
        ).to_dict()
        
        novo_usuario["codigo"] = str(random.randint(100000, 999999))
        novo_usuario["confirmation_timestamp"] = time.time()
        
        pending_users.append(novo_usuario)
        self.pending_db.save(pending_users)
        
        corpo_email = f"""Olá, {novo_usuario['nome']},\n\nCódigo: {novo_usuario['codigo']}"""
        
        if self.email_service.send_email(novo_usuario['email'], "Confirmação de Cadastro", corpo_email):
            return {"status": "sucesso", "mensagem": "Código enviado!"}
        return {"status": "erro", "mensagem": "Erro ao enviar e-mail."}

    def verificacao(self):
        try:
            pending_users = self.pending_db.load()
            users = [UserAccount.from_dict(u) for u in self.user_db.load()]
            
            email = request.forms.get('email')
            codigo = request.forms.get('codigo')
            
            pending_user = next((u for u in pending_users if u['email'] == email and u['codigo'] == codigo), None)
            
            if pending_user:
                user = UserAccount(
                    nome=pending_user['nome'],
                    data_nascimento=pending_user['data_nascimento'],
                    telefone=pending_user['telefone'],
                    email=pending_user['email'],
                    senha=pending_user['senha'],
                    foto_perfil=pending_user['foto_perfil']
                )
                
                users.append(user)
                self.user_db.save([u.to_dict() for u in users])
                pending_users = [u for u in pending_users if u['email'] != email]
                self.pending_db.save(pending_users)
                
                return {"status": "sucesso", "mensagem": "Cadastro confirmado!"}
            return {"status": "erro", "mensagem": "Código incorreto."}
            
        except Exception as e:
            print(f"Erro na verificação: {e}")
            response.status = 500
            return {"status": "erro", "mensagem": "Erro interno"}

    def finalizar_compra(self):
        user_email = self.get_session_id()
        if not user_email:
            return {"status": "erro", "mensagem": "Usuário não logado!"}

        users = self.user_db.load()
        produtos = self.product_db.load()
        user_index = next((i for i, u in enumerate(users) if u['email'] == user_email), None)
        
        if user_index is None:
            return {"status": "erro", "mensagem": "Usuário não encontrado!"}
        
        user = UserAccount.from_dict(users[user_index])
        pedido = {
            "id": str(uuid.uuid4()),
            "data": datetime.now().isoformat(),
            "cliente": user_email,
            "produtos": [],
            "total": 0,
            "status": "pendente"
        }

        for produto_id, quantidade in user.carrinho.items():
            produto = next((p for p in produtos if str(p['id']) == produto_id), None)
            if produto:
                pedido['produtos'].append({
                    "id": produto_id,
                    "nome": produto['nome'],
                    "quantidade": quantidade,
                    "preco_unitario": produto['preco']
                })
                pedido['total'] += produto['preco'] * quantidade

        self.order_db.add_order(pedido)
        user.carrinho = {}
        users[user_index] = user.to_dict()
        self.user_db.save(users)

        return {"status": "sucesso", "mensagem": "Compra finalizada!", "pedido_id": pedido['id']}
    
    def enviar_notificacao(self, mensagem):
        if self.sio:
            self.sio.emit('notificacao', {"mensagem": mensagem})
    
    def check_login(self):
        user_email = self.get_session_id()  
        user_data = self.user_db.find_by_email(user_email)
        
        if user_data:
            user = UserAccount.from_dict(user_data)
            return {"logged_in": True, "name": user.nome}
        return {"logged_in": False}
    
    def logout(self):
        response.delete_cookie("user", secret="chave_secreta") 
        return redirect('/')
    
    def allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS