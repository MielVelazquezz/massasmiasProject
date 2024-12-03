from fastapi import APIRouter, HTTPException, Depends
from models.avaliacao import AvaliacaoDB
from models.usuario import UsuarioDB
from schemas.avaliacao import AvaliacaoCreate, AvaliacaoRead, AvaliacaoReadList
from datetime import datetime
from auth import get_current_user  # Importando a função para obter o usuário atual

router = APIRouter(prefix='/avaliacoes', tags=['AVALIAÇÕES'])

# Criar nova avaliação
@router.post(path='', response_model=AvaliacaoRead)
def criar_avaliacao(nova_avaliacao: AvaliacaoCreate, current_user: UsuarioDB = Depends(get_current_user)):
    nova_avaliacao.data_avaliacao = datetime.now()
    nova_avaliacao.usuario_id = current_user.id_usuario
    try:
        avaliacao = AvaliacaoDB.create(**nova_avaliacao.dict())
        return avaliacao
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao criar avaliação: {str(e)}")


# Listar todas avaliações
@router.get(path='', response_model=AvaliacaoReadList)
def listar_avaliacoes():
    avaliacoes = AvaliacaoDB.select()
    return {'avaliacoes': list(avaliacoes)}

# Listar uma avaliação específica
@router.get(path='/{avaliacao_id}', response_model=AvaliacaoRead)
def listar_uma_avaliacao(avaliacao_id: int):
    avaliacao = AvaliacaoDB.get_or_none(AvaliacaoDB.id_avaliacao == avaliacao_id)
    if not avaliacao:
        raise HTTPException(status_code=404, detail="Avaliação não encontrada")
    return avaliacao

# Excluir avaliação
@router.delete(path='/{avaliacao_id}', response_model=AvaliacaoRead)
def excluir_avaliacao(avaliacao_id: int):
    avaliacao = AvaliacaoDB.get_or_none(AvaliacaoDB.id_avaliacao == avaliacao_id)
    if not avaliacao:
        raise HTTPException(status_code=404, detail="Avaliação não encontrada")
    # Adicione uma verificação para garantir que o usuário atual pode excluir a avaliação, se necessário.
    avaliacao.delete_instance()
    return avaliacao

@router.post("/comentarios/")
async def registrar_comentario(novo_comentario: AvaliacaoCreate, current_user: UsuarioDB = Depends(get_current_user)):
    # Usa o ID do usuário logado (current_user.id_usuario) em vez de receber do form
    novo_comentario.usuario_id = current_user.id_usuario
    comentario = AvaliacaoDB.create(**novo_comentario.model_dump())
    return {"message": "Comentário registrado com sucesso!"}
