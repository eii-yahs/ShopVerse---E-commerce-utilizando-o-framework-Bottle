<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ShopVerse</title>
    <link rel="stylesheet" href="/static/css/style.css">

    <!--Ícones-->
        <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0" />
        <link rel="shortcut icon" type="image/x-icon" href="/static/img/logo.png">
</head>
<body>

    % rebase('html/base.tpl')
    <main>
        <h2 class="marca">PCs Samsung</h2>
        <div class="carrossel-container" id="carrosselApple">
            <button class="carrossel-nav carrossel-prev" onclick="moveCarrossel(-1, 'carrosselApple')">&#10094;</button>
            <div class="carrossel">
                <ul class="produto">
                    % for produto in produtos:
                        <li>
                            <img src="/static/img/produtos/{{ produto['imagem'] }}" alt="{{ produto['nome'] }}" class="produto-imagem">
                            <h3>{{ produto['nome'] }}</h3>
                            <p>{{ produto['descricao'] }}</p>
                            <p>R$ {{ produto['preco'] }}</p>
                            <p><strong>Estoque disponível: <span id="estoque-{{ produto['id'] }}-principal">{{ produto['estoque'] }}</span></strong></p>
                            <div><a href="/produto/{{ produto['id'] }}">Ver detalhes</a></div>
                        </li>
                    % end
                </ul>
            </div>
            <button class="carrossel-nav carrossel-next" onclick="moveCarrossel(1, 'carrosselApple')">&#10095;</button>
        </div>
    <main>

<script src="https://cdn.socket.io/4.6.1/socket.io.min.js"></script>
<script src="/static/js/script.js"></script>
</body>
</html>