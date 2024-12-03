from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
import os

from models.prato import PratoDB
from schemas.prato import PratoCreate, PratoUpdate, PratoRead, PratoReadList

router = APIRouter(
    prefix='/pratos', tags=['PRATOS']
)

@router.post('', response_model=PratoRead)
async def criar_prato(
        nome_prato: str = Form(...),
        valor_prato: float = Form(...),
        imagem_prato: UploadFile = File(...),
        descricao_prato: str = Form(...),
        id_categoria_prato: int = Form(...)
):
    os.makedirs('images', exist_ok=True)

    caminho_imagem = os.path.join('images', imagem_prato.filename)

    with open(caminho_imagem, 'wb') as f:
        f.write(await imagem_prato.read())

    prato = PratoDB.create(
        nome_prato=nome_prato,
        valor_prato=valor_prato,
        imagem_prato=caminho_imagem,
        descricao_prato=descricao_prato,
        id_categoria_prato=id_categoria_prato
    )
    return prato

@router.get("/images/{image_name}")
async def get_image(image_name: str):
    image_path = os.path.join("images", image_name)
    if os.path.exists(image_path):
        return FileResponse(image_path)
    raise HTTPException(status_code=404, detail="Imagem não encontrada")


@router.get(path='', response_model=PratoReadList)
def listar_pratos(search: str = None, category: int = None):
    query = PratoDB.select()

    if search:
        query = query.where(PratoDB.nome_prato.contains(search))
    if category:
        query = query.where(PratoDB.id_categoria_prato == category)

    pratos = list(query)
    return {'pratos': pratos}



@router.get(path='/{id_prato}', response_model=PratoRead)
def obter_prato(id_prato: int):
    prato = PratoDB.get_or_none(PratoDB.id_prato == id_prato)
    if not prato:
        raise HTTPException(status_code=404, detail="Prato não encontrado")
    return prato



@router.patch(path='/{id_prato}', response_model=PratoRead)
async def atualizar_prato(
    id_prato: int,
    nome_prato: str = Form(...),
    valor_prato: float = Form(...),
    descricao_prato: str = Form(...),
    id_categoria_prato: int = Form(...),
    imagem_prato: UploadFile = File(None)
):
    prato = PratoDB.get_or_none(PratoDB.id_prato == id_prato)
    if not prato:
        raise HTTPException(status_code=404, detail="Prato não encontrado")

    prato.nome_prato = nome_prato
    prato.valor_prato = valor_prato
    prato.descricao_prato = descricao_prato
    prato.id_categoria_prato = id_categoria_prato

    if imagem_prato:
        caminho_imagem = os.path.join('images', imagem_prato.filename)
        with open(caminho_imagem, 'wb') as f:
            f.write(await imagem_prato.read())
        prato.imagem_prato = caminho_imagem

    prato.save()
    return prato

@router.delete(path='/{id_prato}', response_model=PratoRead)
def excluir_prato(id_prato: int):
    prato = PratoDB.get_or_none(PratoDB.id_prato == id_prato)
    if not prato:
        raise HTTPException(status_code=404, detail="Prato não encontrado")

    prato.delete_instance()
    return prato
