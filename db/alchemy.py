from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.engine.url import URL
import settings

from models import *
engine = create_engine(URL.create(**settings.DATABASE), pool_pre_ping=True)
Base.metadata.create_all(engine, checkfirst=True)
