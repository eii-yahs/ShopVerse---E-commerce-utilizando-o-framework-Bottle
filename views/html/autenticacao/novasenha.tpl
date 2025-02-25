<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Nova Senha</title>
    <link rel="stylesheet" href="/static/css/style.css">
    <link rel="shortcut icon" type="image/x-icon" href="/static/img/logo.png">
</head>
<body>
    <h1 id="logoname">ShopVerse</h1>
    <div class="page">
        <div class="login">
            <form method="post" id="novaSenhaForm" onsubmit="event.preventDefault(); atualizarSenha();">
                <h1>Redefinir senha</h1>
                <p>Digite sua nova senha:</p>
                <input type="password" id="nova_senha" placeholder="Nova senha" required>
                <p>Digite novamente sua senha:</p>
                <input type="password" id="confirmar_senha" placeholder="Confirme a senha" required>
                <input id="att" type="submit" value="Atualizar senha">
            </form>
        </div>
    </div>
    <footer>© Todos os direitos reservados - ShopVerse - 2025</footer>
    <script src="/static/js/script.js"></script>
</body>
</html>
