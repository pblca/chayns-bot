from sqlalchemy import create_engine, Column, Integer, String, DateTime, BigInteger
from sqlalchemy.orm import relationship

from . import Base


class Guild(Base):

    __tablename__ = 'guilds'
    id = Column(BigInteger, primary_key=True)
    channels = relationship('Channel', back_populates='guild')
