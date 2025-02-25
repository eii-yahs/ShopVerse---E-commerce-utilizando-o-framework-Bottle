<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Login</title>
    <link rel="stylesheet" href="/static/css/style.css">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <link rel="shortcut icon" type="image/x-icon" href="/static/img/logo.png">
</head>
<body>
    <h1 id="logoname">ShopVerse</h1>
<div class="page">
    <div class="login">
        <form id="loginForm">
            <h1>Login</h1>
            <p>Email</p>
            <input type="email" id="email" placeholder="Digite seu email" required>
            <p>Senha</p>
            <div style="position: relative;">
                <input type="password" id="senha" placeholder="Digite sua senha" required>
                <button type="button" id="toggleSenha" style="position: absolute; right: 10px; top: 50%; transform: translateY(-50%); background: none; border: none; cursor: pointer;">👁️</button>
            </div>
            <p><a class="link" href="/senha">Esqueci minha senha</a></p>
            <p class="link">Ainda não possui uma conta? <a href="/cadastro">Crie sua conta aqui</a></p>
            <input id="bot" type="submit" value="Entrar">
            <br>
        </form>
    </div>
</div>
<footer>© Todos os direitos reservados - ShopVerse - 2025</footer>
<script src="/static/js/script.js"></script>
</body>
</html>
