from enum import Enum
from pydantic import BaseModel, constr, Field
from datetime import date

class TipoUsuario(str, Enum):
    cliente = '0'
    admin = '1'
    ser_supremo = '2'
    visitante = '3'

class UsuarioCreate(BaseModel):
    nome_usuario: str
    email_usuario: str
    telefone_usuario: str
    data_nascimento: date
    endereco_usuario: str
    senha_usuario: str
    tipo_usuario: TipoUsuario

class UsuarioUpdate(BaseModel):
    nome_usuario: str
    email_usuario: str
    telefone_usuario: str
    endereco_usuario: str
    senha_usuario: str = Field(default=None, nullable=True)
    tipo_usuario: TipoUsuario

class UsuarioRead(BaseModel):
    id_usuario: int
    nome_usuario: str
    email_usuario: str
    telefone_usuario: str
    data_nascimento: date
    endereco_usuario: str
    tipo_usuario: TipoUsuario

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    tipo_usuario: TipoUsuario
    id_usuario: int

class UsuarioReadWithAvaliacao(BaseModel):
    id_usuario: int
    nome_usuario: str
    email_usuario: str

class UsuarioReadPedido(BaseModel):
    id_usuario: int
    nome_usuario: str
    telefone_usuario: str
    endereco_usuario: str

class UsuarioReadReserva(BaseModel):
    id_usuario: int
    nome_usuario: str
    telefone_usuario: str
    email_usuario: str

class UsuarioReadList(BaseModel):
    usuarios: list[UsuarioRead]
