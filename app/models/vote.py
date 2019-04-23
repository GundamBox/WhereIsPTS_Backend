import datetime
import math

from sqlalchemy import (Column, ForeignKey, Integer, PrimaryKeyConstraint,
                        Sequence, and_)
from sqlalchemy.orm import relationship

from app.commom.database import Base, db


class Vote(Base):
    __table__name = 'vote'

    def __init__(self, sid, cid, vote_count):
        self.sid = sid
        self.cid = cid
        self.vote_count = vote_count

    sid = Column('sid', Integer, ForeignKey('store.id'), primary_key=True)
    cid = Column('cid', Integer, ForeignKey('channel.id'), primary_key=True)
    vote_count = Column(Integer,
                        nullable=False,
                        default=0)

    channel = relationship("Channel", back_populates="stores", uselist=False)
    store = relationship("Store", back_populates="votes", uselist=False)

    @classmethod
    def read(cls, sid, cid):
        return cls.query \
            .filter(Vote.sid == sid) \
            .filter(Vote.cid == cid).first()

    @classmethod
    def read_list(cls, sid):
        return cls.query \
            .filter(Vote.sid == sid) \
            .first() \
            .order_by(Vote.cid) \
            .all()
