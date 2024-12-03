from peewee import Model, AutoField, CharField, DateField
from config.database import database

class UsuarioDB(Model):
    id_usuario = AutoField()
    nome_usuario = CharField(unique=True)
    email_usuario = CharField(unique=True)
    telefone_usuario = CharField(max_length=15, unique=True)
    data_nascimento = DateField()
    endereco_usuario = CharField()
    senha_usuario = CharField()
    tipo_usuario = CharField()

    class Meta:
        database = database
        table_name = 'usuarios'
