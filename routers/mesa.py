from fastapi import APIRouter

from models.mesa import MesaDB
from schemas.mesa import (
    MesaRead,
    MesaCreate,
    MesaReadList,
    MesaUpdate
)

router = APIRouter(
    prefix='/mesas', tags=['MESAS']
)


@router.post(path='', response_model=MesaRead)
def criar_mesa(nova_mesa: MesaCreate):
    mesa = MesaDB.create(**nova_mesa.model_dump())
    return mesa


@router.get(path='', response_model=MesaReadList)
def listar_mesas():
    mesas = MesaDB.select()
    return {'mesas': mesas}


@router.get(path='/{id_mesa}', response_model=MesaRead)
def listar_mesa_por_id(id_mesa: int):
    mesa = MesaDB.get_or_none(MesaDB.id_mesa == id_mesa)
    return mesa


@router.patch(path='/{id_mesa}', response_model=MesaRead)
def atualizar_mesa(id_mesa: int, mesa_atualizada: MesaUpdate):
    mesa = MesaDB.get_or_none(MesaDB.id_mesa == id_mesa)
    if mesa:
        mesa.codigo_mesa = mesa_atualizada.codigo_mesa
        mesa.numero_cadeiras = mesa_atualizada.numero_cadeiras
        mesa.save()
    return mesa


@router.delete(path='/{id_mesa}', response_model=MesaRead)
def excluir_mesa(id_mesa: int):
    mesa = MesaDB.get_or_none(MesaDB.id_mesa == id_mesa)
    if mesa:
        mesa.delete_instance()
    return mesa
