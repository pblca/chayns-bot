from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from . import Base


class Guild(Base):

    __tablename__ = 'guilds'
    id = Column(Integer, primary_key=True)
    channels = relationship('Channel', back_populates='guild')
