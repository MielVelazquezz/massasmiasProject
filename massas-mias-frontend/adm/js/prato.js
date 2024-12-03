// Função para carregar categorias de pratos (GET)
async function carregarCategorias() {
    const response = await fetch('http://localhost:8000/categorias_prato');
    const categorias = await response.json();

    const categoriaSelect = document.getElementById('tipo');
    categoriaSelect.innerHTML = '<option selected disabled>Escolha a categoria</option>';

    categorias.categorias_prato.forEach(categoria => {
        const option = document.createElement('option');
        option.value = categoria.id_categoria_prato;
        option.textContent = categoria.nome_categoria_prato;
        categoriaSelect.appendChild(option);
    });
}

// Função para carregar pratos cadastrados (GET)
async function carregarPratos() {
    try {
        const response = await fetch('http://localhost:8000/pratos');
        if (!response.ok) {
            throw new Error('Erro ao carregar os pratos');
        }
        const pratos = await response.json();

        console.log(pratos); // Adicione este log para verificar a estrutura do JSON

        const pratosBody = document.getElementById('pratos-body');
        const pratosCount = document.getElementById('pratos-count');
        pratosBody.innerHTML = '';

        pratosCount.textContent = pratos.length; // Atualiza o número de pratos

        pratos.forEach(prato => {
            const linha = document.createElement('tr');
            linha.innerHTML = `
                <td>${prato.nome_prato || 'N/A'}</td>
                <td>R$ ${prato.valor_prato ? prato.valor_prato.toFixed(2) : '0.00'}</td>
                <td>
                    <img src="${prato.imagem_prato || 'images/default.png'}" alt="${prato.nome_prato}" class="prato-img" width="50">
                </td>
                <td>${prato.id_categoria_prato.nome_categoria_prato || 'N/A'}</td>
                <td>${prato.descricao_prato || 'N/A'}</td>
                <td>
                    <button class="edit-btn" onclick="editarPrato(${prato.id_prato})"><span class="material-symbols-outlined">edit</span></button>
                    <button class="delete-btn" onclick="excluirPrato(${prato.id_prato})"><span class="material-symbols-outlined">delete</span></button>
                </td>
            `;
            pratosBody.appendChild(linha);
        });
    } catch (error) {
        console.error('Erro:', error);
    }
}

// Função para cadastrar novo prato (POST)
document.getElementById('formCadastro').addEventListener('submit', async (e) => {
    e.preventDefault();

    const nomePrato = document.getElementById('nome').value;
    const descricaoPrato = document.getElementById('descricao').value;
    const imagemPrato = document.getElementById('imagem').files[0];
    const valorPrato = parseFloat(document.getElementById('valor').value);
    const categoriaPrato = parseInt(document.getElementById('tipo').value);

    const formData = new FormData();
    formData.append('nome_prato', nomePrato);
    formData.append('descricao_prato', descricaoPrato);
    formData.append('valor_prato', valorPrato);
    formData.append('imagem_prato', imagemPrato);
    formData.append('id_categoria_prato', categoriaPrato);

    try {
        const response = await fetch('http://localhost:8000/pratos', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error("Erro ao cadastrar o prato");
        }

        window.location = "/massas-mias/admin/feito"
    } catch (error) {
        console.error(error);
        alert("Ocorreu um erro ao cadastrar o prato.");
    }
});

// Função para editar prato (GET)
async function editarPrato(id) {
    try {
        const response = await fetch(`http://localhost:8000/pratos/${id}`);
        const prato = await response.json();

        document.getElementById('nome').value = prato.nome_prato;
        document.getElementById('descricao').value = prato.descricao_prato;
        document.getElementById('valor').value = prato.valor_prato;
        document.getElementById('tipo').value = prato.id_categoria_prato;

        // Alterar o evento de submit do formulário para editar o prato
        document.getElementById('formCadastro').onsubmit = async (e) => {
            e.preventDefault();

            const formData = new FormData();
            formData.append('nome_prato', document.getElementById('nome').value);
            formData.append('descricao_prato', document.getElementById('descricao').value);
            formData.append('valor_prato', parseFloat(document.getElementById('valor').value));
            formData.append('id_categoria_prato', parseInt(document.getElementById('tipo').value));

            try {
                const response = await fetch(`http://localhost:8000/pratos/${id}`, {
                    method: 'PUT',
                    body: formData
                });

                if (!response.ok) {
                    throw new Error("Erro ao editar o prato");
                }

                alert("Prato editado com sucesso!");
                window.location.reload(); // Recarrega a página para atualizar a lista de pratos
            } catch (error) {
                console.error(error);
                alert("Ocorreu um erro ao editar o prato.");
            }
        };
    } catch (error) {
        console.error("Erro ao buscar prato:", error);
    }
}

// Função para excluir prato (DELETE)
async function excluirPrato(id) {
    if (confirm("Tem certeza que deseja excluir este prato?")) {
        try {
            const response = await fetch(`http://localhost:8000/pratos/${id}`, {
                method: 'DELETE'
            });

            if (!response.ok) {
                throw new Error("Erro ao excluir o prato");
            }

            alert("Prato excluído com sucesso!");
            window.location.reload(); // Recarrega a página para atualizar a lista de pratos
        } catch (error) {
            console.error(error);
            alert("Ocorreu um erro ao excluir o prato.");
        }
    }
}

// Carregar dados ao inicializar a página
document.addEventListener('DOMContentLoaded', () => {
    carregarCategorias();
    carregarPratos(); // Carregar pratos cadastrados
});
