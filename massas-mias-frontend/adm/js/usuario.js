// Função para carregar usuários no início
async function carregarDadosUsuarios() {
    await carregarUsuarios();
}

// Função para carregar usuários (GET)
async function carregarUsuarios() {
    const response = await fetch('http://localhost:8000/usuarios');
    const usuarios = await response.json();

    const usuariosCount = document.getElementById('usuarios-count');
    usuariosCount.textContent = usuarios.length; // Atualiza o número de usuários

    carregarTabelaUsuarios(usuarios); // Exibe os usuários na tabela
}

// Função para carregar a tabela de usuários
function carregarTabelaUsuarios(usuarios) {
    const usuariosTableBody = document.querySelector('.usuarios-table tbody');
    usuariosTableBody.innerHTML = ''; // Limpa o corpo da tabela antes de carregar

    usuarios.forEach(usuario => {
        const row = document.createElement('tr');
        
        row.innerHTML = `
            <td>${usuario.nome_usuario}</td>
            <td>${usuario.email_usuario}</td>
            <td>${usuario.telefone_usuario}</td>
            <td>${new Date(usuario.data_nascimento).toLocaleDateString('pt-BR')}</td>
            <td>${usuario.endereco_usuario}</td>
            <td><span class="material-symbols-outlined password-icon">visibility_off</span></td>
            <td>${usuario.tipo_usuario}</td>
            <td>
                <button class="edit-btn" onclick="editarUsuario(${usuario.id_usuario})"><span class="material-symbols-outlined">edit</span></button>
                <button class="delete-btn" onclick="deletarUsuario(${usuario.id_usuario})"><span class="material-symbols-outlined">delete</span></button>
            </td>
        `;

        usuariosTableBody.appendChild(row);
    });
}

// Função para cadastrar novo usuário (CREATE)
document.querySelector('form')?.addEventListener('submit', async (e) => {
    e.preventDefault(); // Impede o envio padrão do formulário

    const nomeUsuario = document.getElementById('nome-completo').value;
    const telefoneUsuario = document.getElementById('telefone').value;
    const emailUsuario = document.getElementById('email').value;
    const dataNascimento = document.getElementById('data-nascimento').value;
    const enderecoUsuario = document.getElementById('endereco').value;
    const senhaUsuario = document.getElementById('senha').value;
    const tipoUsuario = document.getElementById('tipo-usuario').value;

    if (!nomeUsuario || !telefoneUsuario || !emailUsuario || !dataNascimento || !enderecoUsuario || !senhaUsuario || tipoUsuario === "Escolha o tipo de usuário") {
        alert("Por favor, preencha todos os campos.");
        return;
    }

    const usuario = {
        nome_usuario: nomeUsuario,
        telefone_usuario: telefoneUsuario,
        email_usuario: emailUsuario,
        data_nascimento: new Date(dataNascimento).toISOString(),
        endereco_usuario: enderecoUsuario,
        senha_usuario: senhaUsuario,
        tipo_usuario: tipoUsuario
    };

    try {
        const response = await fetch('http://localhost:8000/usuarios', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(usuario)
        });

        if (!response.ok) {
            throw new Error("Erro ao cadastrar o usuário");
        }

        window.location.href = '/massas-mias/admin/feito';
        carregarUsuarios(); // Atualiza a lista de usuários
    } catch (error) {
        console.error(error);
        alert("Ocorreu um erro ao cadastrar o usuário.");
    }
});

// Função para editar usuário (EDIT)
async function editarUsuario(idUsuario) {
    const response = await fetch(`http://localhost:8000/usuarios/${idUsuario}`);
    const usuario = await response.json();

    document.getElementById('nome-completo').value = usuario.nome_usuario;
    document.getElementById('telefone').value = usuario.telefone_usuario;
    document.getElementById('email').value = usuario.email_usuario;
    document.getElementById('data-nascimento').value = usuario.data_nascimento.split('T')[0]; // Ajusta para exibir a data corretamente
    document.getElementById('endereco').value = usuario.endereco_usuario;
    document.getElementById('senha').value = usuario.senha_usuario;
    document.getElementById('tipo-usuario').value = usuario.tipo_usuario;

    const formButton = document.querySelector('form button');
    formButton.textContent = 'Salvar Alterações';
    formButton.onclick = async (e) => {
        e.preventDefault();
        await atualizarUsuario(idUsuario);
    };
}

// Função para atualizar o usuário (UPDATE)
async function atualizarUsuario(idUsuario) {
    const nomeUsuario = document.getElementById('nome-completo').value;
    const telefoneUsuario = document.getElementById('telefone').value;
    const emailUsuario = document.getElementById('email').value;
    const dataNascimento = document.getElementById('data-nascimento').value;
    const enderecoUsuario = document.getElementById('endereco').value;
    const senhaUsuario = document.getElementById('senha').value;
    const tipoUsuario = document.getElementById('tipo-usuario').value;

    const usuario = {
        nome_usuario: nomeUsuario,
        telefone_usuario: telefoneUsuario,
        email_usuario: emailUsuario,
        data_nascimento: new Date(dataNascimento).toISOString(),
        endereco_usuario: enderecoUsuario,
        senha_usuario: senhaUsuario,
        tipo_usuario: tipoUsuario
    };

    try {
        const response = await fetch(`http://localhost:8000/usuarios/${idUsuario}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(usuario)
        });

        if (!response.ok) {
            throw new Error("Erro ao atualizar o usuário");
        }

        window.location.href = '/massas-mias/admin/feito';
        carregarUsuarios(); // Atualiza a lista de usuários
    } catch (error) {
        console.error(error);
        alert("Ocorreu um erro ao atualizar o usuário.");
    }
}

// Função para deletar usuário (DELETE)
async function deletarUsuario(idUsuario) {
    if (confirm("Você tem certeza que deseja deletar este usuário?")) {
        try {
            const response = await fetch(`http://localhost:8000/usuarios/${idUsuario}`, {
                method: 'DELETE'
            });

            if (!response.ok) {
                throw new Error("Erro ao deletar o usuário");
            }

            carregarUsuarios(); // Atualiza a lista de usuários
        } catch (error) {
            console.error(error);
            alert("Ocorreu um erro ao deletar o usuário.");
        }
    }
}

// Chama a função para carregar os usuários quando a página é carregada
document.addEventListener('DOMContentLoaded', carregarDadosUsuarios);
