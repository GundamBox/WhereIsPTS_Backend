import datetime
import math

from sqlalchemy import Column, Integer, Sequence, String
from sqlalchemy.orm import relationship

from app.common.database import Base, db

from .vote import Vote


class Channel(Base):
    __table__name = 'channel'

    cid = Column('id', Integer, Sequence('channel_id_seq'), primary_key=True)
    name = Column(String(128), nullable=False)

    stores = relationship("Vote", back_populates="channel")

    @classmethod
    def read(cls, cid):
        return cls.query \
            .filter(Channel.cid == cid) \
            .first()

    @classmethod
    def read_list(cls):
        return cls.query \
            .order_by(Channel.name) \
            .all()
