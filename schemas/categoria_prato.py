from pydantic import BaseModel


class CategoriaPratoCreate(BaseModel):
    nome_categoria_prato: str


class CategoriaPratoUpdate(BaseModel):
    nome_categoria_prato: str


class CategoriaPratoRead(BaseModel):
    id_categoria_prato: int
    nome_categoria_prato: str


class CategoriaPratoReadList(BaseModel):
    categorias_prato: list[CategoriaPratoRead]