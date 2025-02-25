<!DOCTYPE html>
<html lang="pt-BR"> <!-- Recomendo alterar para português -->
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ produto['nome'] }}</title> <!-- Título dinâmico -->
    <link rel="stylesheet" href="/static/css/style.css">
    <link rel="shortcut icon" type="image/x-icon" href="/static/img/logo.png">
</head>
<body>
    % rebase('html/base.tpl')

    <main class="prod">
        <h2>{{ produto['nome'] }}</h2>
        <img src="/static/img/produtos/{{ produto['imagem'] }}" alt="{{ produto['nome'] }}" style="max-width: 300px;">
        <p>{{ produto['descricao'] }}</p>
        <p><strong>Preço: R$ {{ produto['preco'] }}</strong></p>
        <p><strong>Estoque disponível: <span id="estoque-{{ produto['id'] }}">{{ produto['estoque'] }}</span></strong></p>
        
        <form onsubmit="event.preventDefault(); adicionarAoCarrinho(event, '{{ produto['id'] }}')">
            <label for="quantidade">Quantidade:</label>
            <input 
                type="number" 
                id="quantidade" 
                value="1" 
                min="1"
                max="{{ produto['estoque'] }}" 
            >
            <button type="submit">Adicionar ao Carrinho</button>
        </form>

        <div class="voltar-inicio">
            <a href="/">
                <span class="material-symbols-outlined">arrow_back_ios</span>
                Voltar para a página inicial
            </a>
        </div>
    </main>

    <script src="https://cdn.socket.io/4.6.1/socket.io.min.js"></script>
    <script src="/static/js/script.js"></script>
</body>
</html>