<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Perfil</title>
    <link rel="stylesheet" href="/static/css/style.css">

    <!-- Ícones -->
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0" />
    <link rel="shortcut icon" type="image/x-icon" href="/static/img/logo.png">
</head>
<body>
    % rebase('html/base.tpl')
        <section class="perfil2">
            <div class="info">
                <h1>Olá, {{ user['nome'] }}!</h1>
                <img src="{{ user['foto_perfil'] if user.get('foto_perfil') else '/static/img/perfil/perfil.png' }}" alt="Foto de Perfil" id="foto">
                <p><strong>Nome:</strong> {{ user['nome'] }}</p>
                <p><strong>E-mail:</strong> {{ user['email'] }}</p>
                <p><strong>Telefone:</strong> {{ user['telefone'] }}</p>
                <p><strong>Data de Nascimento:</strong> {{ user['data_nascimento'] }}</p>
                <div id="editar">
                    <a href="editar_perfil" class="edit">Editar perfil</a>
                </div>
            </div>
        </section>
    <script src="/static/js/script.js"></script>
</body>
</html>
