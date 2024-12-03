from fastapi import APIRouter, HTTPException, Depends
from peewee import fn
from schemas.dashboard import DashboardRead, Estatisticas, PedidoPendentes
from models.avaliacao import AvaliacaoDB
from models.pedido import PedidoDB
from models.prato import PratoDB
from models.reserva import ReservaDB
from models.usuario import UsuarioDB
from auth import (
    get_user_by_email_or_phone,
    create_access_token,
    authenticate_user,
    is_admin,   # Certifique-se que está implementado
    is_root,    # Certifique-se que está implementado
    get_user_from_token,
    get_current_user,
    oauth2_scheme
)

router = APIRouter()

@router.get("/dashboard", response_model=DashboardRead)
async def get_dashboard(token: str = Depends(oauth2_scheme)):
    usuario = get_user_from_token(token)

    if not (is_admin(usuario) or is_root(usuario)):
        raise HTTPException(status_code=403, detail="Acesso negado. Usuário não autorizado.")

    # Agregações e contagens para o dashboard
    numero_pedidos = PedidoDB.select().count()
    numero_pratos = PratoDB.select().count()
    numero_reservas = ReservaDB.select().count()
    numero_usuarios = UsuarioDB.select().count()

    lucro_total = (
            PedidoDB
            .select(fn.SUM(PratoDB.valor_prato))  # Soma o preço dos pratos associados
            .join(PratoDB, on=(PedidoDB.prato_id == PratoDB.id_prato))  # Faz a junção entre Pedido e Prato
            .where(PedidoDB.status_pedido == 2)  # Filtra pelo status 'enviado'
            .scalar() or 0  # Retorna 0 caso não haja nenhum pedido 'enviado'
    )

    estatisticas = Estatisticas(
        numero_pedidos=numero_pedidos,
        lucro_total=lucro_total,  # Inclui o lucro total no dashboard
        numero_pratos=numero_pratos,
        numero_reservas=numero_reservas,
        numero_usuarios=numero_usuarios
    )

    # Busca os pedidos pendentes
    pedidos_pendentes = (
        PedidoDB.select()
        .where(PedidoDB.status_pedido == '0')
    )

    # Prepara a lista de pedidos pendentes
    # Modifique o mapeamento dos pedidos pendentes para refletir corretamente os campos
    pedidos_pendentes_list = [
        PedidoPendentes(
            id=pedido.id_pedido,
            nome=pedido.prato_id.nome_prato,  # Nome do prato
            descricao=pedido.prato_id.descricao_prato,  # Descrição do prato
            status=pedido.status_pedido,
            imagem=pedido.prato_id.imagem_prato
        )
        for pedido in pedidos_pendentes
    ]

    # Retorna o conteúdo do dashboard
    return DashboardRead(
        estatisticas=estatisticas,
        pedidos_pendentes=pedidos_pendentes_list
    )
