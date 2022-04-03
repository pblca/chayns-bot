from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base

from db import models, settings

Base = declarative_base()


def init():
    engine = create_engine(URL.create(**settings.DATABASE), pool_pre_ping=True)
    Base.metadata.create_all(engine, checkfirst=True)
    return engine
