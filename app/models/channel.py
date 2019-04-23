import datetime
import math

from sqlalchemy import Column, Integer, Sequence, String
from sqlalchemy.orm import relationship

from app.commom.database import Base, Serializer, db


class Channel(Base, Serializer):
    __table__name = 'channel'

    cid = Column('id', Integer, Sequence('channel_id_seq'), primary_key=True)
    name = Column(String(128), nullable=False)

    votes = relationship("Vote",
                         back_populates="channel")

    @classmethod
    def read(cls, cid):
        return cls.query \
            .filter(Channel.id == cid) \
            .first()

    @classmethod
    def read_list(cls):
        return cls.query \
            .order_by(Channel.name) \
            .all()
