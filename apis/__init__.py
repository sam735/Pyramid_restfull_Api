from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker
from apis.db import initialize_sql
#from apis.db.procedure_model import MyModel


def db(request):
    maker = request.registry.dbmaker
    session = maker()

    def cleanup(request):
        if request.exception is not None:
            session.rollback()
        else:
            session.commit()
        session.close()
    request.add_finished_callback(cleanup)

    return session



def main(global_config, **settings):
    config = Configurator(settings=settings)
    #config.scan('apis.procedure')
    engine = engine_from_config(settings, 'sqlalchemy.')
    #initialize_sql(engine)
    config.registry.dbmaker = sessionmaker(bind=engine)
    config.add_request_method(db, reify=True)
    config.include('apis.routes')
    config.scan('apis.procedure.procedure_controller')
    return config.make_wsgi_app()