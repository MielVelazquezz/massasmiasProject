document.addEventListener("DOMContentLoaded", () => {
    carregarUsuarios();
    carregarPratos();
    carregarStatus();
});

function carregarUsuarios() {
    fetch('http://localhost:8000//usuarios') // Exemplo de endpoint
        .then(response => response.json())
        .then(data => {
            const usuarioSelect = document.getElementById('usuario');
            data.usuarios.forEach(usuario => {
                let option = document.createElement('option');
                option.value = usuario.id;
                option.text = usuario.nome;
                usuarioSelect.add(option);
            });
        })
        .catch(error => console.error('Erro ao carregar usuários:', error));
}

function carregarPratos() {
    fetch('http://localhost:8000//pratos') // Exemplo de endpoint
        .then(response => response.json())
        .then(data => {
            const pratoSelect = document.getElementById('prato');
            data.pratos.forEach(prato => {
                let option = document.createElement('option');
                option.value = prato.id;
                option.text = prato.nome;
                pratoSelect.add(option);
            });
        })
        .catch(error => console.error('Erro ao carregar pratos:', error));
}

function carregarStatus() {
    const statusSelect = document.getElementById('status');
    const statusOptions = {
        '0': 'Pendente',
        '1': 'Em Andamento',
        '2': 'Enviado',
        '3': 'Cancelado'
    };

    Object.entries(statusOptions).forEach(([value, text]) => {
        let option = document.createElement('option');
        option.value = value;
        option.text = text;
        statusSelect.add(option);
    });
}

function cadastrarPedido(event) {
    event.preventDefault();

    const usuario_id = document.getElementById('usuario').value;
    const prato_id = document.getElementById('prato').value;
    const status_pedido = document.getElementById('status').value;
    const data_pedido = document.getElementById('data').value;

    const pedidoData = {
        usuario_id: parseInt(usuario_id),
        prato_id: parseInt(prato_id),
        status_pedido: status_pedido,
        data_pedido: new Date(data_pedido).toISOString()
    };

    fetch('/pedidos', { // Exemplo de endpoint
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(pedidoData)
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('pedidoForm').reset(); // Limpa o formulário
        // Você pode redirecionar ou atualizar a lista de pedidos aqui, se necessário
    })
    .catch((error) => {
        console.error('Erro ao cadastrar pedido:', error);
        alert('Erro ao cadastrar pedido. Tente novamente.');
    });
}
