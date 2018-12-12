
from db import db
from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker

def main(global_config, **settings):
    config = Configurator(settings=settings)
    engine = engine_from_config(settings, 'sqlalchemy.')
    config.registry.dbmaker = sessionmaker(bind=engine)
    config.add_request_method(db, reify=True)
    config.include('apis.routes')
    config.scan('apis.procedure.procedure_controller')
    return config.make_wsgi_app()