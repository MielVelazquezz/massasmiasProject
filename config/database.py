from peewee import SqliteDatabase

database = SqliteDatabase('database.db')


def startup_db():
    database.connect()

    from models.avaliacao import AvaliacaoDB
    from models.categoria_prato import CategoriaPratoDB
    from models.mesa import MesaDB
    from models.pedido import PedidoDB
    from models.prato import PratoDB
    from models.reserva import ReservaDB
    from models.usuario import UsuarioDB

    database.create_tables(
        [
            AvaliacaoDB,
            CategoriaPratoDB,
            MesaDB,
            PedidoDB,
            PratoDB,
            ReservaDB,
            UsuarioDB
        ]
    )


def shutdown_db():
    database.close()