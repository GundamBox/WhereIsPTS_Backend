import datetime
import math

from sqlalchemy import ForeignKey, PrimaryKeyConstraint, Sequence

from app.commom.database import Base, Serializer, db


class Votes(Base, Serializer):
    __table__name = 'votes'

    store_id = db.Column(db.Integer, ForeignKey('store.id'))
    news_id = db.Column(db.Integer, ForeignKey('news.id'))
    vote_count = db.Column(db.Integer,
                           nullable=False,
                           default=0)
    __table_args__ = (
        PrimaryKeyConstraint('store_id', 'news_id'),
    )
