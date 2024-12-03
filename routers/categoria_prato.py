from fastapi import APIRouter

from models.categoria_prato import CategoriaPratoDB
from schemas.categoria_prato import (
    CategoriaPratoRead,
    CategoriaPratoCreate,
    CategoriaPratoReadList,
    CategoriaPratoUpdate
)

router = APIRouter(
    prefix='/categorias_prato', tags=['CATEGORIAS DE PRATO']
)


@router.post(path='', response_model=CategoriaPratoRead)
def criar_categoria_prato(novo_tipo: CategoriaPratoCreate):
    categoria_prato = CategoriaPratoDB.create(**novo_tipo.model_dump())
    return categoria_prato


@router.get(path='', response_model=CategoriaPratoReadList)
def listar_categorias_prato():
    categorias_prato = CategoriaPratoDB.select()
    return {'categorias_prato': categorias_prato}


@router.get(path='/{id_categoria_prato}', response_model=CategoriaPratoRead)
def listar_categoria_prato_por_id(id_categoria_prato: int):
    categoria_prato = CategoriaPratoDB.get_or_none(
        CategoriaPratoDB.id_categoria_prato == id_categoria_prato
    )
    return categoria_prato


@router.patch(path='/{id_categoria_prato}', response_model=CategoriaPratoRead)
def atualizar_categoria_prato(
    id_categoria_prato: int, tipo_atualizado: CategoriaPratoUpdate
):
    categoria_prato = CategoriaPratoDB.get_or_none(
        CategoriaPratoDB.id_categoria_prato == id_categoria_prato
    )
    if categoria_prato:
        categoria_prato.nome_categoria_prato = tipo_atualizado.nome_categoria_prato
        categoria_prato.save()
    return categoria_prato


@router.delete(path='/{id_categoria_prato}', response_model=CategoriaPratoRead)
def excluir_categoria_prato(id_categoria_prato: int):
    categoria_prato = CategoriaPratoDB.get_or_none(
        CategoriaPratoDB.id_categoria_prato == id_categoria_prato
    )
    if categoria_prato:
        categoria_prato.delete_instance()
    return categoria_prato
