from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from . import Base


class Channel(Base):

    __tablename__ = 'channels'
    id = Column(Integer, primary_key=True)
    guild_id = Column(Integer, ForeignKey('guilds.id'))
    mirror_to_channel_id = Column(Integer, ForeignKey('channels.id'), nullable=True)
    guild = relationship("Guild", back_populates="channels")
