<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Cadastro</title>
    <link rel="stylesheet" href="/static/css/style.css">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <link rel="shortcut icon" type="image/x-icon" href="/static/img/logo.png">
</head>
<body>
    <h1 id="logoname">ShopVerse</h1>
    <div class="page2">
        <div class="cad">
            <form id="registerForm">
                <h1>Cadastro</h1>

                <p>Nome completo</p>
                <input type="text" id="nome" placeholder="Digite seu nome e sobrenome" required>

                <p>Data de Nascimento</p>
                <input type="date" id="data_nascimento" required>

                <p>Telefone</p>
                <input type="text" id="telefone" placeholder="(00) 00000-0000" required>

                <p>Email</p>
                <input type="email" id="email" placeholder="Digite seu email" required>
                
                <p>Senha</p>
                <div style="position: relative;">
                    <input type="password" id="senha" placeholder="Digite sua senha" required oninput="validatePassword()">
                    <button type="button" id="toggleSenha1" style="position: absolute; right: 10px; top: 50%; transform: translateY(-50%); background: none; border: none; cursor: pointer;">👁️</button>
                </div>
                <div id="senha-avisos">
                    <p id="length" class="requirement">Mínimo 8 caracteres <span class="icon"></span></p>
                    <p id="uppercase" class="requirement">Letra maiúscula <span class="icon"></span></p>
                    <p id="number" class="requirement">Número <span class="icon"></span></p>
                    <p id="special" class="requirement">Caractere especial (@, #, $, etc.) <span class="icon"></span></p>
                </div>

                <p>Confirme sua senha</p>
                <div style="position: relative;">
                    <input type="password" id="confirma_senha" placeholder="Digite novamente sua senha" required oninput="validatePassword()">
                    <button type="button" id="toggleSenha2" style="position: absolute; right: 10px; top: 50%; transform: translateY(-50%); background: none; border: none; cursor: pointer;">👁️</button>
                </div>
                <div id="confirma-senha-aviso">
                    <p id="senha-igual">As senhas devem ser iguais <span class="icon"></span></p>
                </div>
                <p class="link">Já possui uma conta? <a href="/login">Faça login</a></p>
                <input id="criar" type="submit" value="Criar conta">
            </form>
        </div>
    </div>
    <footer>© Todos os direitos reservados - ShopVerse - 2025</footer>
    <script src="/static/js/script.js"></script>
</body>
</html>
