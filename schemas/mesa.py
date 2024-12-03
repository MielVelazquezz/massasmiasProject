from pydantic import BaseModel, Field

class MesaCreate(BaseModel):
    codigo_mesa: str
    numero_cadeiras: int = Field(ge=0, le=8)

class MesaUpdate(BaseModel):
    codigo_mesa: str
    numero_cadeiras: int = Field(ge=0, le=8)

class MesaRead(BaseModel):
    id_mesa: int
    codigo_mesa: str
    numero_cadeiras: int = Field(ge=0, le=8)

class MesaReadList(BaseModel):
    mesas: list[MesaRead]