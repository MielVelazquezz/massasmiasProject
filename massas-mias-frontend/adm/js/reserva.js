// Função para carregar mesas, usuários e reservas no início
async function carregarDados() {
    await carregarMesas();
    await carregarUsuarios();
    await carregarReservas();
}

// Função para carregar mesas (GET)
async function carregarMesas() {
    const response = await fetch('http://localhost:8000/mesas');
    const mesas = await response.json();
    
    const mesaSelect = document.getElementById('mesa');
    mesaSelect.innerHTML = '<option selected>Escolha a mesa</option>';
    
    mesas.mesas.forEach(mesa => { // Acessa a lista de mesas
        const option = document.createElement('option');
        option.value = mesa.id_mesa; // Mudado para id_mesa
        option.textContent = mesa.codigo_mesa; // Mudado para codigo_mesa
        mesaSelect.appendChild(option);
    });
}

// Função para carregar usuários (GET)
async function carregarUsuarios() {
    const response = await fetch('http://localhost:8000/usuarios');
    const usuarios = await response.json();

    const usuarioSelect = document.getElementById('usuario');
    usuarioSelect.innerHTML = '<option selected>Escolha o usuário</option>';

    usuarios.usuarios.forEach(usuario => { // Acessa a lista de usuários
        const option = document.createElement('option');
        option.value = usuario.id_usuario; // Mudado para id_usuario
        option.textContent = usuario.nome_usuario; // Mudado para nome_usuario
        usuarioSelect.appendChild(option);
    });
}

// Função para carregar reservas (GET)
async function carregarReservas() {
    const response = await fetch('http://localhost:8000/reservas');
    const reservas = await response.json();

    const reservasTableBody = document.querySelector('.reservas-table tbody');
    reservasTableBody.innerHTML = ''; // Limpa o corpo da tabela antes de carregar

    reservas.reservas.forEach(reserva => {
        const row = document.createElement('tr');
        
        row.innerHTML = `
            <td>${reserva.mesa_id.codigo_mesa}</td>
            <td>${new Date(reserva.data_reservada).toLocaleDateString('pt-BR')}</td>
            <td>${reserva.usuario_id.nome_usuario}</td>
            <td>${reserva.numero_pessoas || 1}</td> <!-- Assumindo 1 como default, ajuste conforme seu schema -->
            <td>
                <button class="edit-btn"><span class="material-symbols-outlined">edit</span></button>
                <button class="delete-btn" onclick="deletarReserva(${reserva.id_reserva})"><span class="material-symbols-outlined">delete</span></button>
            </td>
        `;

        reservasTableBody.appendChild(row);
    });
}

// Função para cadastrar nova reserva (CREATE)
document.querySelector('form').addEventListener('submit', async (e) => {
    e.preventDefault(); // Impede o envio padrão do formulário

    const mesa = document.getElementById('mesa').value;
    const dataReservada = document.getElementById('data').value;
    const usuario = document.getElementById('usuario').value;

    if (mesa === "Escolha a mesa" || usuario === "Escolha o usuário" || !dataReservada) {
        alert("Por favor, preencha todos os campos.");
        return;
    }

    const reserva = {
        usuario_id: parseInt(usuario), // Mudado para usuario_id
        mesa_id: parseInt(mesa), // Mudado para mesa_id
        data_reservada: new Date(dataReservada).toISOString() // Formato ISO para datetime
    };

    try {
        const response = await fetch('http://localhost:8000/reservas', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(reserva)
        });

        if (!response.ok) {
            throw new Error("Erro ao cadastrar a reserva");
        }


        window.location.href = '/massas-mias/admin/feito';
    } catch (error) {
        console.error(error);
        alert("Ocorreu um erro ao cadastrar a reserva.");
    }
});


// Função para deletar reserva (DELETE)
async function deletarReserva(idReserva) {
    const confirmacao = confirm("Você tem certeza que deseja deletar esta reserva?");
    if (!confirmacao) return;

    try {
        const response = await fetch(`http://localhost:8000/reservas/${idReserva}`, {
            method: 'DELETE',
        });

        if (!response.ok) {
            throw new Error("Erro ao deletar a reserva");
        }

        alert("Reserva deletada com sucesso!");
        carregarReservas(); // Atualiza a lista de reservas
    } catch (error) {
        console.error(error);
        alert("Ocorreu um erro ao deletar a reserva.");
    }
}

// Carregar dados ao inicializar a página
carregarDados();
