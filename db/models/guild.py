from sqlalchemy import Column, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


class Guild(declarative_base()):
    __tablename__ = 'guilds'
    id = Column(BigInteger, primary_key=True)
    channels = relationship('Channel', back_populates='guild')
