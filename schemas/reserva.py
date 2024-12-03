from pydantic import BaseModel
from datetime import datetime
from schemas.usuario import UsuarioReadReserva  # Assumindo que você tenha esse schema
from schemas.mesa import MesaRead  # Assumindo que você tenha esse schema

class ReservaCreate(BaseModel):
    usuario_id: int
    mesa_id: int
    data_reservada: datetime

class ReservaUpdate(BaseModel):
    mesa_id: int
    data_reservada: datetime

class ReservaRead(BaseModel):
    id_reserva: int
    usuario_id: UsuarioReadReserva  # Referenciando o schema de leitura de Usuario
    mesa_id: MesaRead  # Referenciando o schema de leitura de Mesa
    data_reservada: datetime

class ReservaReadList(BaseModel):
    reservas: list[ReservaRead]
