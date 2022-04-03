from sqlalchemy import Column, BigInteger
from sqlalchemy.orm import relationship

from db.setup import Base


class Guild(Base):
    __tablename__ = 'guilds'
    id = Column(BigInteger, primary_key=True)
    channels = relationship('Channel', back_populates='guild')
