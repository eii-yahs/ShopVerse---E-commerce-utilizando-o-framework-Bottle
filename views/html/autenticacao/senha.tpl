<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Recuperar Senha</title>
    <link rel="stylesheet" href="/static/css/style.css">
    <link rel="shortcut icon" type="image/x-icon" href="/static/img/logo.png">
</head>
<body>
    <h1 id="logoname">ShopVerse</h1>
    <div class="page">
        <div class="login" id="recuperarSenhaForm">
            <form id="recuperarSenhaForm" onsubmit="event.preventDefault(); recuperarSenha();">
                <h1>Esqueceu a senha?</h1>
                <p>Email</p>
                <input type="email" id="email" placeholder="Digite seu email" required>
                <p><a class="link" href="/login">Continuar login</a></p>
                <p class="link">Ainda não possui uma conta? <a href="/cadastro">Crie sua conta aqui</a></p>
                <input id="senha1" type="submit" value="Enviar Email">
            </form>
        </div>
    </div>

    <footer>© Todos os direitos reservados - ShopVerse - 2025</footer>
    <script src="/static/js/script.js"></script>
</body>
</html>
