self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open('massas-mias-cache').then((cache) => {
            const filesToCache = [
                '/static/index.html',
                '/static/css/style.css',
                '/static/cadastro.html',
                '/static/home.html',
                '/static/mesas.html',
                '/static/manifest.json',
                '/static/images/192x192.png',
                '/static/images/512x512.png',
                '/static/images/144x144.png',
                '/static/adm/pagina-principal.html',
                '/static/adm/listaavaliacoes.html',
                '/static/adm/listacategoria.html',
                '/static/adm/listamesas.html',
                '/static/adm/listapedidos.html',
                '/static/adm/listapratos.html',
                '/static/adm/listareserva.html',
                '/static/adm/listausuarios.html',
                '/static/adm/catpratos.html',
                '/static/adm/mesas.html',
                '/static/adm/pedidos.html',
                '/static/adm/pratos.html',
                '/static/adm/reservas.html',
                '/static/adm/usuarios.html',
                '/static/adm/update_pages/atcategoria.html',
                '/static/adm/update_pages/atmesa.html',
                '/static/adm/update_pages/atpedido.html',
                '/static/adm/update_pages/atprato.html',
                '/static/adm/update_pages/atreserva.html',
                '/static/adm/update_pages/atusuario.html',
                '/static/adm/feito.html',
            ];
            console.log("Arquivos sendo adicionados ao cache:", filesToCache);
            return cache.addAll(filesToCache);
        }).catch((error) => {
            console.error("Erro ao adicionar arquivos ao cache:", error);
        })
    );
});

self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request).then((cachedResponse) => {
            if (cachedResponse) {
                return cachedResponse; // Arquivo encontrado no cache
            }
            return fetch(event.request); // Caso contrário, vai até a rede
        }).catch((error) => {
            console.error("Erro ao buscar o arquivo no cache ou na rede:", error);
        })
    );
});
