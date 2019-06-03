import datetime
import math

from sqlalchemy import Column, Integer, Sequence, String
from sqlalchemy.orm import relationship

from app.common.database import Base, db
from app.common.exception import FlaskException

from .vote import Vote


class Channel(Base):
    __table__name = 'channel'

    cid = Column('id', Integer, Sequence('channel_id_seq'), primary_key=True)
    name = Column(String(128), nullable=False)

    stores = relationship("Vote", back_populates="channel")

    @classmethod
    def read(cls, cid):
        channel =  cls.query \
            .filter(Channel.cid == cid) \
            .first()
        if channel:
            return channel
        else:
            raise FlaskException(message='Store not found', status_code=404)

    @classmethod
    def read_list(cls):
        return cls.query \
            .order_by(Channel.name) \
            .all()
