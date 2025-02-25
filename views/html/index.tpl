<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ShopVerse</title>
    <link rel="stylesheet" href="/static/css/style.css">

    <!-- Ícones -->
    <link rel="shortcut icon" type="image/x-icon" href="/static/img/logo.png">
</head>
<body>
    % rebase('html/base.tpl')
    <main>
        % for categoria, produtos in categorias.items():
        <h2 class="marca">{{ categoria }}</h2>
        <div class="carrossel-container" id="carrossel{{ categoria }}">
            <button class="carrossel-nav carrossel-prev" onclick="moveCarrossel(-1, 'carrossel{{ categoria }}')">&#10094;</button>
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
            <button class="carrossel-nav carrossel-next" onclick="moveCarrossel(1, 'carrossel{{ categoria }}')">&#10095;</button>
        </div>
    % end

    </main>
    <script src="https://cdn.socket.io/4.6.1/socket.io.min.js"></script>
    <script src="/static/js/script.js"></script>
</body>
</html>
