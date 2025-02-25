from bottle import Bottle, static_file
import os
import socketio
import eventlet.wsgi
import eventlet
import threading
import time
from controllers.variables import pending_db
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from controllers.application import Application

#----------------Inicia a Aplicação----------------
app = Bottle()
# Configuração do Socket.IO
sio = socketio.Server(async_mode='eventlet')
application = Application(sio)
app_with_socketio = socketio.WSGIApp(sio, app)

# ---------------ROTAS ESTÁTICAS---------------
@app.route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='static')

# ----------------ROTAS DE INTERFACE----------------
@app.route('/')
def index():
    return application.render('index')

@app.route('/login')
def login_page():
    return application.render('login')

@app.route('/cadastro')
def cadastro_page():
    return application.render('cadastro')

@app.route('/verificacao')
def verificacao_page():
    return application.render('verificacao')

@app.route('/editar_perfil', method=['GET', 'POST'])
def editar_perfil():
    return application.render('editar_perfil')

@app.route('/senha', method='GET')
def verificacao_form():
    return application.render('senha')

@app.route('/recuperar_senha', method='POST')
def recuperar_senha():
    return application.recuperar_senha()

@app.route('/novasenha/<token>', method=['GET', 'POST'])
def novasenha(token):
    return application.render('novasenha', token)

@app.route('/macbooks')
def macbooks():
    return application.render('macbooks')

@app.route('/iphone')
def iphone():
    return application.render('iphone')

@app.route('/pcsamsung')
def pcsamsung():
    return application.render('pcsamsung')

@app.route('/celsamsung')
def celsamsung():
    return application.render('celsamsung')

@app.route('/perfil')
def perfil():
    return application.render('perfil')

@app.route('/produto/<id>')
def produto(id):
    return application.render('produto', id)

@app.route('/carrinho')
def visualizar_carrinho():
    return application.render('carrinho')

#-------------------POSTS-------------------
@app.post('/adicionar_ao_carrinho')
def handle_adicionar():
    return application.render('adicionar_ao_carrinho', is_post=True)

@app.post('/remover_do_carrinho')
def handle_remover():
    return application.render('remover_do_carrinho', is_post=True)

@app.post('/login')
def handle_login():
    return application.render('login', is_post=True)

@app.post('/cadastro')
def handle_cadastro():
    return application.render('cadastro', is_post=True)

@app.post('/verificacao')
def handle_verificacao():
    return application.render('verificacao', is_post=True)

@app.post('/finalizar_compra')
def handle_finalizar():
    return application.render('finalizar_compra', is_post=True)
    
#-------------------------GETTERS-------------------------
@app.get('/check_login')
def check_login():
    return application.check_login()

@app.get('/logout')
def logout():
    return application.logout()

#-------------------------SOCKET.IO-------------------------
@sio.on('connect')
def connect(sid, environ):
    print(f'Cliente conectado: {sid}')
    
def limpar_usuarios_pendentes_periodicamente():
    while True:
        pending_db.remover_usuarios_expirados()
        time.sleep(60) 
    
# Iniciando o servidor
if __name__ == "__main__":
    threading.Thread(target=limpar_usuarios_pendentes_periodicamente, daemon=True).start()
    
    eventlet.wsgi.server(eventlet.listen(("127.0.0.1", 5000)), app_with_socketio)