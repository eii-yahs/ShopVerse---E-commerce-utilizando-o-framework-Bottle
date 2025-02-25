<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ShopVerse</title>
    <link rel="stylesheet" href="/static/css/style.css">

    <!-- Ícones -->
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0" />
    <head>
    <link rel="shortcut icon" type="image/x-icon" href="/static/img/logo.png">
</head>

</head>
<body>
    <header>
        <nav class="menu">
        
        <div class="bmenu"></div>
        
        <div class="perfil" id="userProfile">
            <h3 id="userName"></h3>
            <div class="img">
                <img src="{{ user['foto_perfil'] if user.get('foto_perfil') else '/static/img/perfil/perfil.png' }}" alt="Foto de Perfil" class="img">
            </div>
        </div>

        <div class="bomenu">
            <a href="perfil"><span class="material-symbols-outlined">person</span> Perfil</a>
            <a href="carrinho"><span class="material-symbols-outlined">shopping_cart</span> Carrinho</a>
            <a href="" onclick="logout()"><span class="material-symbols-outlined">logout</span> Sair</a>
        </div>
        <div id="authButtons">
            <a href="/login" class="lc">Login</a>
            <a href="/cadastro" class="lc">Criar Conta</a>
        </div>


        <div class="aba">
            <a href="/"><span class="material-symbols-outlined">home</span> Página Inicial</a>
            <details>
                <summary><span class="material-symbols-outlined">computer</span> Computadores</summary>
                <a href="macbooks" id="mnl"><span class="material-symbols-outlined">ios</span> MacBook</a>
                <a href="pcsamsung" id="mnl"><span class="material-symbols-outlined">android</span> Samsung</a>
            </details>
            <details>
                <summary><span class="material-symbols-outlined">smartphone</span> Celulares</summary>
                <a href="iphone" id="mnl"><span class="material-symbols-outlined">ios</span> iPhone</a>
                <a href="celsamsung" id="mnl"><span class="material-symbols-outlined">android</span> Samsung</a>
            </details>
        </div>
    </nav>

    </header>

    <main>
        {{!base}}
    </main>

    <footer>© Todos os direitos reservados - ShopVerse - 2025</footer>
    <script src="/static/js/script.js"></script>
</body>
</html>