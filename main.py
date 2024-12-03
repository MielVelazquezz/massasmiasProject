from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles  # Importar StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from datetime import datetime

from config.database import shutdown_db, startup_db
from routers.avaliacao import router as avaliacao_router
from routers.categoria_prato import router as categoria_prato_router
from routers.mesa import router as mesa_router
from routers.pedido import router as pedido_router
from routers.prato import router as prato_router
from routers.reserva import router as reserva_router
from routers.usuario import router as usuario_router
import os  # Importar os para manipulação de caminho
from routers.dashboard import router as dashboard_router

app = FastAPI(title='MASSAS MIAS')

app.add_event_handler(event_type='startup', func=startup_db)
app.add_event_handler(event_type='shutdown', func=shutdown_db)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/images", StaticFiles(directory=os.path.join(os.getcwd(), "images")), name="images")
# O de casa ⬇
app.mount("/static", StaticFiles(directory=os.path.join(os.getcwd(), "massas-mias-frontend")), name="static")


# O do SENAI ⬇
# app.mount("/static", StaticFiles(directory=os.path.join(os.getcwd(), "massas-mias-frontend")), name="static")


@app.get('/massas-mias', response_class=HTMLResponse)
async def index():
    return FileResponse("massas-mias-frontend/index.html")

@app.get('/massas-mias/home', response_class=HTMLResponse)
async def home():
    return FileResponse("massas-mias-frontend/home.html")

@app.get('/massas-mias/cadastro', response_class=HTMLResponse)
async def cadastro():
    return FileResponse("massas-mias-frontend/cadastro.html")


@app.get('/massas-mias/reservas', response_class=HTMLResponse)
async def pagina_reservas():
    return FileResponse("massas-mias-frontend/mesas.html")


# Página dos Admin ⬇️
@app.get('/massas-mias/admin', response_class=HTMLResponse)
async def home_admin():
    return FileResponse("massas-mias-frontend/adm/pagina-principal.html")

@app.get('/massas-mias/admin/avaliacoes', response_class=HTMLResponse)
async def avaliacao_admin():
    return FileResponse("massas-mias-frontend/adm/listaavaliacoes.html")

@app.get('/massas-mias/admin/categorias-pratos', response_class=HTMLResponse)
async def categoria_prato_admin():
    return FileResponse("massas-mias-frontend/adm/listacategoria.html")

@app.get('/massas-mias/admin/mesas', response_class=HTMLResponse)
async def mesas_admin():
    return FileResponse("massas-mias-frontend/adm/listamesas.html")

@app.get('/massas-mias/admin/pedidos', response_class=HTMLResponse)
async def pedidos_admin():
    return FileResponse("massas-mias-frontend/adm/listapedidos.html")

@app.get('/massas-mias/admin/pratos', response_class=HTMLResponse)
async def pratos_admin():
    return FileResponse("massas-mias-frontend/adm/listapratos.html")

@app.get('/massas-mias/admin/reservas', response_class=HTMLResponse)
async def reservas_admin():
    return FileResponse("massas-mias-frontend/adm/listareserva.html")

@app.get('/massas-mias/admin/usuarios', response_class=HTMLResponse)
async def usuario_admin():
    return FileResponse("massas-mias-frontend/adm/listausuarios.html")

# CAMPOS DE ADICIONAR
@app.get('/massas-mias/admin/categorias-pratos/adicionar', response_class=HTMLResponse)
async def home():
    return FileResponse("massas-mias-frontend/adm/catpratos.html")

@app.get('/massas-mias/admin/mesas/adicionar', response_class=HTMLResponse)
async def adicionar_mesas():
    return FileResponse("massas-mias-frontend/adm/mesas.html")

@app.get('/massas-mias/admin/pedidos/adicionar', response_class=HTMLResponse)
async def adicionar_pedidos():
    return FileResponse("massas-mias-frontend/adm/pedidos.html")

@app.get('/massas-mias/admin/pratos/adicionar', response_class=HTMLResponse)
async def adicionar_pratos():
    return FileResponse("massas-mias-frontend/adm/pratos.html")

@app.get('/massas-mias/admin/reservas/adicionar', response_class=HTMLResponse)
async def adicionar_reservas():
    return FileResponse("massas-mias-frontend/adm/reservas.html")

@app.get('/massas-mias/admin/usuarios/adicionar', response_class=HTMLResponse)
async def adicionar_usuarios():
    return FileResponse("massas-mias-frontend/adm/usuarios.html")

@app.get('/massas-mias/admin/categorias-pratos/atualizar', response_class=HTMLResponse)
async def atualizar_categoria_prato():
    return FileResponse("massas-mias-frontend/adm/update_pages/atcategoria.html")
@app.get('/massas-mias/admin/mesas/atualizar', response_class=HTMLResponse)
async def atualizar_mesas():
    return FileResponse("massas-mias-frontend/adm/update_pages/atmesa.html")

@app.get('/massas-mias/admin/pedidos/atualizar', response_class=HTMLResponse)
async def atualizar_pedidos():
    return FileResponse("massas-mias-frontend/adm/update_pages/atpedido.html")

@app.get('/massas-mias/admin/pratos/atualizar', response_class=HTMLResponse)
async def atualizar_pratos():
    return FileResponse("massas-mias-frontend/adm/update_pages/atprato.html")

@app.get('/massas-mias/admin/reservas/atualizar', response_class=HTMLResponse)
async def atualizar_reservas():
    return FileResponse("massas-mias-frontend/adm/update_pages/atreserva.html")

@app.get('/massas-mias/admin/usuarios/atualizar', response_class=HTMLResponse)
async def atualizar_usuarios():
    return FileResponse("massas-mias-frontend/adm/update_pages/atusuario.html")

@app.get('/massas-mias/admin/feito', response_class=HTMLResponse)
async def pagina_feito():
    return FileResponse("massas-mias-frontend/adm/feito.html")



app.include_router(avaliacao_router)
app.include_router(categoria_prato_router)
app.include_router(mesa_router)
app.include_router(pedido_router)
app.include_router(prato_router)
app.include_router(reserva_router)
app.include_router(usuario_router)

app.include_router(dashboard_router)
