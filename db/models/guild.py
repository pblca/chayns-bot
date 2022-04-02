from sqlalchemy import create_engine, Column, Integer, String, DateTime
from . import Base


class Guild(Base):

    __tablename__ = 'guilds'
    id = Column(Integer, primary_key=True)
