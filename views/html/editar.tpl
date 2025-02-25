<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Editar Perfil</title>
    <link rel="stylesheet" href="/static/css/style.css">

    <link rel="shortcut icon" type="image/x-icon" href="/static/img/logo.png">
</head>
<body>
    % rebase('html/base.tpl')

    <main>
        <div id="editar_perfil">
            <h2>Editar Perfil</h2>

            <form action="/editar_perfil" method="POST" enctype="multipart/form-data">
                <div class="foto-perfil-container">
                    <img src="{{ user['foto_perfil'] if user.get('foto_perfil') else '/static/img/perfil/perfil.png' }}" alt="Foto de Perfil" id="foto">
                    <div class="botao-container">
                        <label for="uploadButton" id="upload">Escolher Foto</label>
                        <input type="file" id="uploadButton" name="foto_perfil" accept="image/*" class="uploadButton">

                        <button type="button" id="removerFoto">Remover Foto</button>
                    </div>
                    <input type="hidden" id="remover_foto" name="remover_foto" value="0">
                </div>

                <div class="input-container">
                    <label for="nome">Nome:</label>
                    <input type="text" name="nome" value="{{ user['nome'] }}" required class="input">
                </div>

                <div class="input-container">
                    <label for="telefone">Telefone:</label>
                    <input type="text" name="telefone" value="{{ user['telefone'] }}" required class="input">
                </div>

                <div class="input-container">
                    <label for="data_nascimento">Data de Nascimento:</label>
                    <input type="date" name="data_nascimento" value="{{ user['data_nascimento'] }}" required class="input">
                </div>

                <button type="submit">Salvar Alterações</button>
            </form>
        </div>
    </main>

    <script src="/static/js/script.js"></script>
</body>
</html>
