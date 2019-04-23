import datetime
import math

from sqlalchemy import (Column, ForeignKey, Integer, PrimaryKeyConstraint,
                        Sequence, and_)
from sqlalchemy.orm import relationship

from app.commom.database import Base, Serializer, db


class Vote(Base, Serializer):
    __table__name = 'vote'
    __table_args__ = (
        PrimaryKeyConstraint('sid', 'cid'),
    )

    def __init__(self, sid, cid, vote_count=0):
        self.sid = sid
        self.cid = cid
        self.vote_count = vote_count

    sid = Column('sid', Integer, ForeignKey('store.id'))
    cid = Column('cid', Integer, ForeignKey('channel.id'))
    vote_count = Column(Integer,
                        nullable=False,
                        default=0)

    stores = relationship("Store",
                          back_populates="vote")
    channels = relationship("Channel",
                            back_populates="vote")

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
