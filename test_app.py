import pytest
import json
import os
import sys
from webtest import TestApp
from bottle import request
from controllers.application import Application
from route import app as bottle_app
from controllers.variables import (
    TEST_DB_PATH,
    TEST_PENDING_DB_PATH,
    TEST_PRODUCTS_DB_PATH,
    user_db,
    product_db,
    pending_db,
)
from controllers.email_service import EmailService
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from route import app as bottle_app, user_db, product_db, pending_db, EmailService
except ImportError as e:
    raise ImportError(f"Erro ao importar o módulo app: {e}")

application = Application(sio=None)

# Função auxiliar para criar um usuário com todos os campos necessários
def create_full_user(email, senha, nome="Test User"):
    return {
        "email": email,
        "senha": senha,
        "nome": nome,
        "data_nascimento": "2000-01-01",
        "telefone": "123456789",
        "foto_perfil": "/static/img/perfil/default.png",
        "carrinho": {}
    }

# Função auxiliar para criar um usuário pendente com todos os campos necessários
def create_full_pending_user(email, codigo, nome="Test User", senha="Senha123."):
    return {
        "email": email,
        "codigo": codigo,
        "nome": nome,
        "senha": senha,
        "data_nascimento": "2000-01-01",
        "telefone": "123456789",
        "foto_perfil": "/static/img/perfil/default.png",
    }

@pytest.fixture(scope="module")
def setup_test_environment():
    os.makedirs('db', exist_ok=True)
    
    user_db.path = TEST_DB_PATH
    pending_db.path = TEST_PENDING_DB_PATH
    product_db.path = TEST_PRODUCTS_DB_PATH

    with open(TEST_DB_PATH, 'w') as f:
        json.dump([], f)
    with open(TEST_PENDING_DB_PATH, 'w') as f:
        json.dump([], f)
    with open(TEST_PRODUCTS_DB_PATH, 'w') as f:
        json.dump([], f)

    yield

    # Remove os arquivos de teste após a execução dos testes
    os.remove(TEST_DB_PATH)
    os.remove(TEST_PENDING_DB_PATH)
    os.remove(TEST_PRODUCTS_DB_PATH)

@pytest.fixture(scope="module")
def test_app():
    return TestApp(bottle_app)

# Função auxiliar para simular o login e garantir que o cookie seja configurado
def realizar_login(test_app, email, senha):
    usuarios = user_db.load()
    if not any(u['email'] == email for u in usuarios):
        usuarios.append(create_full_user(email, senha))
        user_db.save(usuarios)
    response = test_app.post_json('/login', {"email": email, "senha": senha})
    assert response.status_code == 200
    return response

# Teste de login bem-sucedido
def test_login_successful(setup_test_environment, test_app):
    user_db.save([create_full_user("test@example.com", "Senha123")])
    response = test_app.post_json('/login', {"email": "test@example.com", "senha": "Senha123"})
    assert response.status_code == 200
    assert "Login bem-sucedido!" in response.json['message']

# Teste de login com credenciais inválidas
def test_login_failed(setup_test_environment, test_app):
    user_db.save([])
    response = test_app.post_json('/login', {"email": "wrong@example.com", "senha": "wrongpassword"}, status=401)
    assert response.status_code == 401
    assert "Credenciais inválidas" in response.json['error']

# Teste de cadastro bem-sucedido
def test_cadastro_successful(setup_test_environment, test_app):
    response = test_app.post('/cadastro', {
        "nome": "New User",
        "data_nascimento": "2000-01-01",
        "telefone": "123456789",
        "email": "newuser@example.com",
        "senha": "Senha123!"
    })
    assert response.status_code == 200
    assert "Código enviado!" in response.json['mensagem']

# Teste de cadastro com e-mail duplicado
def test_cadastro_email_duplicado(setup_test_environment, test_app):
    user_db.save([create_full_user("existing@example.com", "Senha123!")])
    response = test_app.post('/cadastro', {
        "nome": "New User",
        "data_nascimento": "2000-01-01",
        "telefone": "123456789",
        "email": "existing@example.com",
        "senha": "Senha1234!"
    })
    assert response.status_code == 200
    assert "E-mail já cadastrado" in response.json['mensagem']

# Teste para adicionar produto ao carrinho (exige usuário logado)
def test_adicionar_ao_carrinho(setup_test_environment, test_app):
    product_db.save([{"id": 1, "nome": "Test Product", "preco": 100, "estoque": 10}])
    realizar_login(test_app, "test@example.com", "Senha123")
    response = test_app.post('/adicionar_ao_carrinho', {
        "produto_id": "1",
        "quantidade": "2"
    })
    assert response.status_code == 200
    assert "Produto adicionado ao carrinho!" in response.json['mensagem']

# Teste para remover produto do carrinho (exige usuário logado)
def test_remover_do_carrinho(setup_test_environment, test_app):
    product_db.save([{"id": 1, "nome": "Test Product", "preco": 100, "estoque": 10}])
    realizar_login(test_app, "test@example.com", "Senha123")
    test_app.post('/adicionar_ao_carrinho', {
        "produto_id": "1",
        "quantidade": "2"
    })
    response = test_app.post('/remover_do_carrinho', {
        "produto_id": "1"
    })
    produto_id = request.forms.get('produto_id')
    produtos = product_db.load()
    produto = next((p for p in produtos if str(p['id']) == produto_id), None)
    assert response.status_code == 200
    assert f"{produto['nome']} removido do carrinho!" in response.json['mensagem']

# Teste de envio de e-mail com sucesso
def test_enviar_email_successful(setup_test_environment):
    result = EmailService.send_email("test@example.com", "Test Subject", "Test Body")
    assert result is True

# Teste de envio de e-mail com credenciais inválidas
def test_enviar_email_failed(setup_test_environment):
    EmailService.SENDER_PASSWORD = "wrongpassword"
    result = EmailService.send_email("test@example.com", "Test Subject", "Test Body")
    assert result is False

# Teste para recuperação de senha com e-mail não cadastrado
def test_recuperar_senha_email_nao_encontrado(setup_test_environment, test_app):
    # Simula uma requisição de recuperação de senha com e-mail não cadastrado
    response = test_app.post_json('/recuperar_senha', {"email": "nonexistent@example.com"}, status=404)
    assert response.status_code == 404
    assert "E-mail não encontrado." in response.json['message']


# Teste para edição de perfil (exige usuário logado)
def test_editar_perfil_successful(setup_test_environment, test_app):
    user_db.save([create_full_user("test@example.com", "senha123")])
    realizar_login(test_app, "test@example.com", "senha123")
    response = test_app.post('/editar_perfil', {
        "nome": "Updated User",
        "foto_perfil": "new_photo.jpg"
    })
    assert response.status_code == 302
    assert response.location == 'http://localhost:80/perfil'

# Teste para verificação de código de confirmação bem-sucedida
def test_verificacao_successful(setup_test_environment, test_app):
    pending_db.save([create_full_pending_user("test@example.com", "123456")])
    response = test_app.post('/verificacao', {
        "email": "test@example.com",
        "codigo": "123456"
    })
    assert response.status_code == 200
    assert "Cadastro confirmado!" in response.json['mensagem']

# Teste para verificação com código incorreto
def test_verificacao_codigo_incorreto(setup_test_environment, test_app):
    pending_db.save([create_full_pending_user("test@example.com", "123456")])
    response = test_app.post('/verificacao', {
        "email": "test@example.com",
        "codigo": "654321"
    })
    assert response.status_code == 200
    assert "Código incorreto" in response.json['mensagem']

# Teste para logout (exige usuário logado)
def test_logout_successful(setup_test_environment, test_app):
    user_db.save([create_full_user("test@example.com", "Senha123.")])
    test_app.post_json('/login', {"email": "test@example.com", "senha": "Senha123."})
    response = test_app.get('/logout')
    assert response.status_code == 302
    assert "user=;" not in response.headers.get('Set-Cookie', '')

# Teste para finalizar compra com sucesso
def test_finalizar_compra_successful(setup_test_environment, test_app):
    produto_teste = {
        "id": 1,
        "nome": "Produto Teste",
        "preco": 50.0,
        "estoque": 10
    }
    product_db.save([produto_teste])

    email = "comprador@example.com"
    senha = "Senha123"
    user_db.save([create_full_user(email, senha)])
    realizar_login(test_app, email, senha)

    test_app.post('/adicionar_ao_carrinho', {
        "produto_id": "1",
        "quantidade": "1"
    })

    response = test_app.post_json('/finalizar_compra', {})

    assert response.status_code == 200
    assert response.json['status'] == 'sucesso'
    assert "Compra finalizada!" in response.json['mensagem']
