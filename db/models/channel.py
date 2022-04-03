from sqlalchemy import Column, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from db.setup import Base


class Channel(Base):
    __tablename__ = 'channels'
    id = Column(BigInteger, primary_key=True)
    guild_id = Column(BigInteger, ForeignKey('guilds.id'))
    mirror_to_channel_id = Column(BigInteger, ForeignKey('channels.id'), nullable=True)
    guild = relationship("Guild", back_populates="channels")
