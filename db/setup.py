from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

from db import models, settings


def init():
    engine = create_engine(URL.create(**settings.DATABASE), pool_pre_ping=True)
    models.Base.metadata.create_all(engine, checkfirst=True)
    return engine
