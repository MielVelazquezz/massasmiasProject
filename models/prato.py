from peewee import AutoField, CharField, DoubleField, ForeignKeyField, Model
from config.database import database
from models.categoria_prato import CategoriaPratoDB

class PratoDB(Model):
    id_prato = AutoField()
    nome_prato = CharField(unique=True)
    valor_prato = DoubleField()
    imagem_prato = CharField()
    descricao_prato = CharField()
    id_categoria_prato = ForeignKeyField(model=CategoriaPratoDB, backref='pratos')


    class Meta:
        database = database
        table_name = 'pratos'