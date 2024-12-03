from peewee import Model, AutoField, IntegerField, CharField
from config.database import database

class MesaDB(Model):
    id_mesa = AutoField()
    codigo_mesa = CharField(unique=True)
    numero_cadeiras = IntegerField()

    class Meta:
        database = database
        table_name = 'mesas'