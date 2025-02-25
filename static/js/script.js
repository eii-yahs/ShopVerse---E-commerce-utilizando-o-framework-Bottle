let currentIndexApple = 0; 
let currentIndexSamsung = 0; 

document.getElementById("loginForm")?.addEventListener("submit", function(e) {
    e.preventDefault();

    const email = document.getElementById("email").value;
    const senha = document.getElementById("senha").value;

    fetch('/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, senha })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            alert(data.message);
            window.location.href = '/';
        }
    });
});

document.addEventListener("DOMContentLoaded", function() {
    let registerForm = document.getElementById("registerForm");

    if (registerForm) {
        registerForm.addEventListener("submit", function(event) {
            event.preventDefault(); 

            let nome = document.getElementById("nome").value;
            let data_nascimento = document.getElementById("data_nascimento").value;
            let telefone = document.getElementById("telefone").value;
            let email = document.getElementById("email").value;
            let senha = document.getElementById("senha").value;
            let confirma_senha = document.getElementById("confirma_senha").value;

            if (senha !== confirma_senha) {
                alert("As senhas não coincidem!");
                return;
            }

            fetch("/cadastro", {
                method: "POST",
                headers: { "Content-Type": "application/x-www-form-urlencoded" },
                body: `nome=${nome}&data_nascimento=${data_nascimento}&telefone=${telefone}&email=${email}&senha=${senha}`
            })
            .then(response => response.json())
            .then(data => {
                alert(data.mensagem);
                if (data.status === "sucesso") {
                    window.location.href = "/verificacao"; 
                }
            })
            .catch(error => console.error("Erro:", error));
        });
    }

    let verifyForm = document.getElementById("verifyForm");

    if (verifyForm) {
        verifyForm.addEventListener("submit", function(event) {
            event.preventDefault();

            let email = document.getElementById("email").value;
            let codigo = document.getElementById("codigo").value;

            fetch("/verificacao", {
                method: "POST",
                headers: { "Content-Type": "application/x-www-form-urlencoded" },
                body: `email=${email}&codigo=${codigo}`
            })
            .then(response => response.json())
            .then(data => {
                alert(data.mensagem);
                if (data.status === "sucesso") {
                    window.location.href = "/login"; 
                }
            });
        });
    }
});

document.addEventListener("DOMContentLoaded", function() {
    function togglePasswordVisibility(input, button) {
        if (input.type === "password") {
            input.type = "text";
            button.textContent = "☁️";
        } else {
            input.type = "password";
            button.textContent = "👁️";
        }
    }

    const loginSenhaInput = document.getElementById("senha");
    const loginToggleSenha = document.getElementById("toggleSenha");

    if (loginSenhaInput && loginToggleSenha) {
        loginToggleSenha.addEventListener("click", function() {
            togglePasswordVisibility(loginSenhaInput, loginToggleSenha);
        });
    }

    const cadastroSenhaInput = document.getElementById("senha");
    const cadastroConfirmaSenhaInput = document.getElementById("confirma_senha");
    const cadastroToggleSenha1 = document.getElementById("toggleSenha1");
    const cadastroToggleSenha2 = document.getElementById("toggleSenha2");

    if (cadastroSenhaInput && cadastroToggleSenha1) {
        cadastroToggleSenha1.addEventListener("click", function() {
            togglePasswordVisibility(cadastroSenhaInput, cadastroToggleSenha1);
        });
    }

    if (cadastroConfirmaSenhaInput && cadastroToggleSenha2) {
        cadastroToggleSenha2.addEventListener("click", function() {
            togglePasswordVisibility(cadastroConfirmaSenhaInput, cadastroToggleSenha2);
        });
    }
});


const perfil = document.querySelector('.perfil');
const menu = document.querySelector('.bomenu');

perfil.onclick = function() {
    menu.classList.toggle('ativo');
}

const menu2 = document.querySelector('.bmenu');
const aba = document.querySelector('.aba'); 

menu2.onclick = function() {
    aba.classList.toggle('ativo');
}

document.addEventListener("DOMContentLoaded", function () {
    let userProfile = document.getElementById("userProfile");
    let authButtons = document.getElementById("authButtons");

    fetch("/check_login")
        .then(response => response.json())
        .then(data => {
            if (data.logged_in) {
                userProfile.style.display = "flex";  
                authButtons.style.display = "none";  
                document.getElementById("userName").innerText = data.name;  

                document.getElementById("perfilLink").addEventListener("click", function() {
                    window.location.href = "/perfil"; 
                });
            } else {
                userProfile.style.display = "none";
                authButtons.style.display = "flex";
            }
        })
        .catch(error => console.error("Erro ao verificar login:", error));
});


function logout() {
    document.cookie = "user=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    window.location.href = "/";
}

var form = document.querySelector('form');
if (form) {  
    form.addEventListener('submit', function(e) {
        var email = document.querySelector('input[name="email"]');
        if (email && !email.value) {  
            e.preventDefault();  
            alert("Por favor, insira um e-mail.");
        }
    });
}


function moveCarrossel(direction, carrosselId) {
    const carrossel = document.getElementById(carrosselId).querySelector('.carrossel');
    const items = carrossel.querySelectorAll('.produto li'); 
    const totalItems = items.length;

    let currentIndex = (carrosselId === 'carrosselApple') ? currentIndexApple : currentIndexSamsung;

    currentIndex += direction;

    if (currentIndex < 0) {
        currentIndex = totalItems - 1;
    } else if (currentIndex >= totalItems) {
        currentIndex = 0;
    }

    if (carrosselId === 'carrosselApple') {
        currentIndexApple = currentIndex;
    } else {
        currentIndexSamsung = currentIndex;
    }

    const itemWidth = items[0].offsetWidth;
    carrossel.style.transform = `translateX(-${currentIndex  * itemWidth}px`;
}

function atualizarSenha() {
    const novaSenha = document.getElementById("nova_senha").value;
    const confirmarSenha = document.getElementById("confirmar_senha").value;

    if (novaSenha !== confirmarSenha) {
        alert("As senhas não coincidem. Tente novamente.");
        return;
    }

    const token = window.location.pathname.split('/').pop();

    fetch(`/novasenha/${token}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nova_senha: novaSenha })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'erro') {
            alert(data.message); 
        } else {
            alert(data.message);
            window.location.href = '/login'; 
        }
    })
    .catch(error => {
        alert('Erro ao fazer a requisição: ' + error.message); 
    });
}


function recuperarSenha() {
    const email = document.getElementById("email").value;

    if (!email) {
        alert("Por favor, insira o e-mail.");
        return;
    }

    fetch('/recuperar_senha', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email })  
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'erro') {
            alert(data.message); 
        } else {
            alert(data.message); 
        }
    })
    .catch(error => {
        alert('Erro ao fazer a requisição: ' + error.message); 
    });
}

document.getElementById("uploadButton")?.addEventListener("change", function(event) {
    const fileInput = event.target;
    const file = fileInput.files[0];

    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById("foto").src = e.target.result; 
        };
        reader.readAsDataURL(file); 

        document.getElementById("upload").innerText = file.name;
    }
});

document.getElementById("removerFoto")?.addEventListener("click", function() {
    const foto = document.getElementById("foto");
    foto.src = '/static/img/perfil/perfil.png'; 

    document.getElementById("remover_foto").value = "1"; 

    document.getElementById("upload").innerText = "Escolher Foto";
});

document.querySelector("form[action='/editar_perfil']")?.addEventListener("submit", function(event) {
});

function adicionarAoCarrinho(event, produtoId) {
    event.preventDefault();

    fetch('/check_login')
    .then(response => response.json())
    .then(loginData => {
        if (!loginData.logged_in) {
            const querLogin = confirm("Você precisa estar logado para adicionar itens ao carrinho.\nDeseja fazer login agora?");
            if (querLogin) {
                window.location.href = '/login';
            }
            return;
        }

        const quantidade = document.getElementById("quantidade").value || 1;

        fetch('/adicionar_ao_carrinho', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: `produto_id=${produtoId}&quantidade=${quantidade}`
        })
        .then(response => {
            if (response.status === 401) {
                throw new Error("Faça login para continuar");
            }
            return response.json();
        })
        .then(data => {
            if (data.status === "erro") {
                alert(data.mensagem);
            } else {
                if (typeof atualizarCarrinho === 'function') {
                    atualizarCarrinho();
                }
                setTimeout(() => {
                    window.location.href = '/';
                }, 200);
            }
        })
        .catch(error => {
            alert(error.message || "Erro ao adicionar ao carrinho!");
        });
    });
}

function removerDoCarrinho(produtoId) {
    fetch('/remover_do_carrinho', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: `produto_id=${produtoId}`
    })
    .then(response => response.json()) 
    .then(data => {
        alert(data.mensagem);
        location.reload();
        const carrinhoItem = document.getElementById(`carrinho-item-${produtoId}`);
        if (carrinhoItem) {
            carrinhoItem.remove();
        }

        const totalElement = document.getElementById('total-carrinho');
        if (totalElement) {
        }
    })
    .catch(error => {
        console.error("Erro:", error);
        alert("Erro ao remover do carrinho!");
    });
}

const socket = io("http://127.0.0.1:5000");

socket.on("connect", () => {
    console.log("Conectado ao WebSocket!");
});

socket.on("notificacao", (data) => {
    alert(data.mensagem); 
});

socket.on("atualizar_estoque", (data) => {
    console.log("Recebido evento de atualização de estoque:", data);
    const produtoId = data.produto_id;
    const estoque = data.estoque;

    const estoqueProduto = document.getElementById(`estoque-${produtoId}`);
    if (estoqueProduto) {
        estoqueProduto.innerText = estoque;
    }

    const estoquePrincipal = document.getElementById(`estoque-${produtoId}-principal`);
    if (estoquePrincipal) {
        estoquePrincipal.innerText = estoque;
    }
});

socket.on("atualizar_carrinho", (data) => {
    console.log("Recebido evento de atualização do carrinho:", data);
    const produtoId = data.produto_id;
    const quantidade = data.quantidade;
    const produto = data.produto;

    const carrinhoItem = document.getElementById(`carrinho-item-${produtoId}`);

    if (carrinhoItem) {
        const quantidadeElement = carrinhoItem.querySelector('.quantidade');
        if (quantidadeElement) {
            quantidadeElement.innerText = quantidade;
        }

        if (quantidade === 0) {
            carrinhoItem.remove();
        }
    }
    
    const totalElement = document.getElementById('total-carrinho');
    if (totalElement) {
    }
});

console.log("Script carregado!"); 


function validatePassword() {
    const password = document.getElementById("senha").value; 
    const length = document.getElementById("length");
    const uppercase = document.getElementById("uppercase");
    const number = document.getElementById("number");
    const special = document.getElementById("special");
    const confirmPassword = document.getElementById("confirma_senha").value;
    const equal = document.getElementById("senha-igual")

    const isLongEnough = password.length >= 8;
    const hasUppercase = /[A-Z]/.test(password);
    const hasNumber = /[0-9]/.test(password);
    const hasSpecial = /[@#$%^&*()_+!.]/.test(password);
    const confirmPass = password === confirmPassword;

    updateRequirement(length, isLongEnough);
    updateRequirement(uppercase, hasUppercase);
    updateRequirement(number, hasNumber);
    updateRequirement(special, hasSpecial);
    
    if (confirmPass) {
        equal.style.color = "green";
        equal.textContent = "As senhas coincidem ✔";
    } else {
        equal.style.color = "red";
        equal.textContent = "As senhas não coincidem ✖";
    }
}

function updateRequirement(element, isValid) {
    const icon = element.querySelector(".icon");
    if (isValid) {
        element.classList.add("valid");
        element.classList.remove("invalid");
        element.style.color = "green";
        icon.innerHTML = "✔"; 
        icon.style.color = "green";
    } else {
        element.classList.add("invalid");
        element.classList.remove("valid");
        element.style.color = "red";
        icon.innerHTML = "✖"; 
        icon.style.color = "red";
    }
}

function finalizarCompra() {
    fetch('/finalizar_compra', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({})
    })
    .then(response => response.json())
    .then(data => {
        alert(data.mensagem);  
        
        if (data.status === 'sucesso') {
            window.location.href = "/";
        }
    })
    .catch(error => console.error('Erro ao finalizar compra:', error));
}
