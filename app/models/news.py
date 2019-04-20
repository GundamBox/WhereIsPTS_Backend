import datetime
import math

from sqlalchemy import Sequence

from app.commom.database import Base, Serializer, db


class News(Base, Serializer):
    __table__name = 'news'

    id = db.Column(db.Integer, Sequence('news_id_seq'), primary_key=True)
    channel_name = db.Column(db.String(128), nullable=False)
