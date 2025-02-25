<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Carrinho de Compras</title>
    <link rel="stylesheet" href="/static/css/style.css"

    <link rel="shortcut icon" type="image/x-icon" href="/static/img/logo.png">
</head>
<body>
    % rebase('html/base.tpl')

        <main class="car">
        <h2>Carrinho de Compras</h2>
        % if produtos:
            <table>
                <thead>
                    <tr>
                        <th></th>
                        <th>Produto</th>
                        <th>Quantidade</th>
                        <th>Preço Unitário</th>
                        <th>Subtotal</th>
                        <th>Ações</th>
                    </tr>
                </thead>
                <tbody>
                    % for produto in produtos:
                        <tr id="carrinho-item-{{ produto['id'] }}">
                            <td><img src="/static/img/produtos/{{ produto['imagem'] }}"></td>
                            <td>{{ produto['nome'] }}</td>
                            <td class="quantidade">{{ produto['quantidade'] }}</td>
                            <td>R$ {{ produto['preco'] }}</td>
                            <td>R$ {{ produto['subtotal'] }}</td>
                            <td>
                            <!-- Botão para remover o produto -->
                            <button onclick="removerDoCarrinho('{{ produto['id'] }}')" id="delete">
                                <span class="material-symbols-outlined">delete</span>
                            </button>
                        </tr>
                    % end
                </tbody>
            </table>
            <p><strong>Total: R$ {{ total }}</strong></p>
            <form action="/finalizar_compra" method="post">
                <button type="submit" class="btn-finalizar" id="btn-finalizar" onclick="finalizarCompra()">
                    Finalizar Compra
                </button>
            </form>
        % else:
            <p id="carrinho-vazio-mensagem">Seu carrinho está vazio.</p>
        % end

        <button><a href="/">Continuar comprando</a></button>

    </main>
    <script src="https://cdn.socket.io/4.6.1/socket.io.min.js"></script>
    <script src="/static/js/script.js"></script>
</body>
</html>