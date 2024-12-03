from pydantic import BaseModel, Field
from datetime import datetime
from schemas.usuario import UsuarioReadWithAvaliacao
# from time import time

class AvaliacaoCreate(BaseModel):
    estrela_avaliacao: int = Field(ge=0, le=5)
    usuario_avaliacao: str
    data_avaliacao: datetime
    usuario_id: int

class AvaliacaoRead(BaseModel):
    id_avaliacao: int
    estrela_avaliacao: int = Field(ge=0, le=5)
    usuario_avaliacao: str
    data_avaliacao: datetime
    # hora_avaliacao: time
    usuario_id: UsuarioReadWithAvaliacao


class AvaliacaoReadList(BaseModel):
    avaliacoes: list[AvaliacaoRead]