from peewee import AutoField, ForeignKeyField, Model, DateField, IntegerField, CharField
from config.database import database
from models.usuario import UsuarioDB



class AvaliacaoDB(Model):
    id_avaliacao = AutoField()
    estrela_avaliacao = IntegerField()
    usuario_avaliacao = CharField()
    usuario_id = ForeignKeyField(model=UsuarioDB, backref='avaliacoes')
    data_avaliacao = DateField()


    class Meta:
        database = database
        table_name = 'avaliacoes'