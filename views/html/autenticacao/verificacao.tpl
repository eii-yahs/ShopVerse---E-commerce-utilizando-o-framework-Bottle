<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Verificação de Email</title>
    <link rel="stylesheet" href="/static/css/style.css">
    <link rel="shortcut icon" type="image/x-icon" href="/static/img/logo.png">
</head>
<body>
    <h1 id="logoname">ShopVerse</h1>
    <div class="page">
        <div class="login">
            <form id="verifyForm">
                <h1>Verificação de Email</h1>
                <p>Email</p>
                <input type="email" id="email" name="email" required />
                <p>Código de Verificação</p>
                <input type="text" id="codigo" name="codigo" required />
                <input id="verif" type="submit" value="Verificar">
            </form>
        </div>
    </div>
    <script src="/static/js/script.js"></script>
</body>
</html>