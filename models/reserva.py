from peewee import AutoField, ForeignKeyField, Model, DateTimeField
from config.database import database
from models.usuario import UsuarioDB
from models.mesa import MesaDB



class ReservaDB(Model):
    id_reserva = AutoField()
    usuario_id = ForeignKeyField(model=UsuarioDB, backref='reservas')
    mesa_id = ForeignKeyField(model=MesaDB, backref='reservas')
    data_reservada = DateTimeField()


    class Meta:
        database = database
        table_name = 'reservas'