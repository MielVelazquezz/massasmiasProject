from peewee import Model, AutoField, CharField
from config.database import database

class CategoriaPratoDB(Model):
    id_categoria_prato = AutoField()
    nome_categoria_prato = CharField(unique=True)

    class Meta:
        database = database
        table_name = 'categorias_prato'