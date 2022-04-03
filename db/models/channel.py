from sqlalchemy import Column, ForeignKey, BigInteger, Integer, Boolean
from sqlalchemy.orm import relationship
from db.setup import Base


class Channel(Base):
    __tablename__ = 'channels'
    id = Column(BigInteger, primary_key=True)
    guild_id = Column(BigInteger, ForeignKey('guilds.id'))
    mirror_to_channel_id = Column(BigInteger, ForeignKey('channels.id'), nullable=True)
    guild = relationship("Guild", back_populates="channels")
    janitor_limit = Column(Integer, nullable=True)
    janitor_frequency = Column(Integer, nullable=True)
    janitor_init_wipe = Column(Boolean, default=False)
