import datetime
import math

from geoalchemy2 import Geometry
from geoalchemy2.functions import ST_Distance_Sphere
from sqlalchemy import (Boolean, Column, DateTime, Float, Integer, Sequence,
                        String, and_)
from sqlalchemy.orm import relationship
from flask import current_app
from app.common.database import Base, db
from app.common.exception import FlaskException
from .vote import Vote


class Store(Base):
    __table__name = 'store'

    sid = Column('id', Integer,
                 Sequence('store_id_seq'),
                 primary_key=True)
    name = Column(String(128),
                  nullable=False)
    location = Column('geom', Geometry('POINT'), nullable=False)
    address = Column(String(256),
                     nullable=True)
    switchable = Column(Boolean,
                        nullable=False)
    enable = Column(Boolean,
                    nullable=False,
                    default=True)
    disable_vote = Column(Integer,
                          nullable=False,
                          default=0)
    last_modified = Column(DateTime,
                           nullable=False,
                           default=datetime.datetime.now)
    last_ip = Column(String(40), nullable=False)

    votes = relationship("Vote", back_populates="store")

    def __init__(self, name, lat, lng, address, switchable, last_ip):
        self.name = name
        self.location = 'POINT({lat} {lng})'.format(lat=lat, lng=lng)
        self.address = address
        self.switchable = switchable
        self.last_ip = last_ip

    @classmethod
    def read(cls, sid: int):
        store = cls.query \
            .filter(Store.sid == sid) \
            .filter(Store.enable == True) \
            .first()
        if store:
            return store
        else:
            raise FlaskException(message='Store not found', status_code=404)

    @classmethod
    def read_list(cls, lat: float, lng: float, name: str, radius: float, page: int, page_size: int):

        radius = max(radius, current_app.config['STORE_SEARCH_MIN_RADIUS'])
        radius = min(radius, current_app.config['STORE_SEARCH_MAX_RADIUS'])

        store_list = cls.query \
            .filter(Store.enable == True) \
            .filter(ST_Distance_Sphere(Store.location, 'POINT({lat} {lng})'.format(lat=lat, lng=lng)) <= radius)

        if name:
            store_list = store_list.filter(Store.name.like('%' + name + '%'))

        store_list = store_list.all()
        count = len(store_list)

        offset = (page-1)*page_size
        store_list = store_list[offset:
                                offset + page_size]

        return store_list, count
