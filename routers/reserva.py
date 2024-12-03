from fastapi import APIRouter, HTTPException
from models.reserva import ReservaDB
from datetime import datetime, timedelta
from schemas.reserva import (
    ReservaCreate,
    ReservaUpdate,
    ReservaRead,
    ReservaReadList,
)

router = APIRouter(
    prefix='/reservas', tags=['RESERVAS']
)

@router.post("/{mesa_id}/disponibilidade")
async def verificar_disponibilidade(mesa_id: int, data: dict):
    try:
        # Parse da data enviada no JSON
        data_reservada = datetime.strptime(data['data_reservada'], "%Y-%m-%dT%H:%M:%S")

        # Intervalo de 5 horas
        inicio_intervalo = data_reservada - timedelta(hours=5)
        fim_intervalo = data_reservada + timedelta(hours=5)

        # Verificar no banco se há conflitos
        reservas_existentes = ReservaDB.select().where(
            (ReservaDB.mesa_id == mesa_id) &
            (ReservaDB.data_reservada >= inicio_intervalo) &
            (ReservaDB.data_reservada <= fim_intervalo)
        )

        return {"disponivel": not reservas_existentes.exists()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao verificar disponibilidade: {str(e)}")

@router.post(path='', response_model=ReservaRead)
def criar_reserva(nova_reserva: ReservaCreate):
    # Verificar se a mesa está disponível para a data e horário
    reserva_existente = ReservaDB.select().where(
        ReservaDB.mesa_id == nova_reserva.mesa_id,
        ReservaDB.data_reservada == nova_reserva.data_reservada
    ).first()

    if reserva_existente:
        raise HTTPException(status_code=400, detail="Mesa já reservada para esse horário.")

    # Criar nova reserva
    reserva = ReservaDB.create(
        usuario_id=nova_reserva.usuario_id,
        mesa_id=nova_reserva.mesa_id,
        data_reservada=nova_reserva.data_reservada
    )

    return reserva


@router.get(path='', response_model=ReservaReadList)
def listar_reservas():
    reservas = ReservaDB.select()
    return {'reservas': reservas}


@router.get(path='/{id_reserva}', response_model=ReservaRead)
def obter_reserva(id_reserva: int):
    reserva = ReservaDB.get_or_none(ReservaDB.id_reserva == id_reserva)
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva não encontrada")
    return reserva


@router.patch(path='/{id_reserva}', response_model=ReservaRead)
def atualizar_reserva(id_reserva: int, reserva_atualizada: ReservaUpdate):
    reserva = ReservaDB.get_or_none(ReservaDB.id_reserva == id_reserva)
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva não encontrada")

    reserva.mesa_id = reserva_atualizada.mesa_id
    reserva.data_reservada = reserva_atualizada.data_reservada
    reserva.save()
    return reserva


@router.delete(path='/{id_reserva}', response_model=ReservaRead)
def excluir_reserva(id_reserva: int):
    reserva = ReservaDB.get_or_none(ReservaDB.id_reserva == id_reserva)
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva não encontrada")

    reserva.delete_instance()
    return reserva
