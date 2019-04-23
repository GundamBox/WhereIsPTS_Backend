import datetime
import math

from sqlalchemy import (Boolean, Column, DateTime, Float, Integer, Sequence,
                        String, and_)
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from geoalchemy2.functions import ST_Distance, ST_AsGeoJSON
from app.commom.database import Base, Serializer, db


class Store(Base, Serializer):
    __table__name = 'store'

    sid = Column('id', Integer,
                 Sequence('store_id_seq'),
                 primary_key=True)
    name = Column(String(128),
                  nullable=False)
    geom = Column(Geometry('POINT'), nullable=False)
    # lat = Column(Float,
    #              nullable=False)
    # lng = Column(Float,
    #              nullable=False)
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

    votes = relationship("Vote",
                         back_populates="store")

    def __init__(self, name, lat, lng, address, switchable, ip):
        self.name = name
        self.geom = 'POINT({lat} {lng})'.format(lat=lat, lng=lng)
        # self.lat = lat
        # self.lng = lng
        self.address = address
        self.switchable = switchable
        self.ip = ip

    def serialize(self):
        json_ser = super().serialize()
        geo_json = ST_AsGeoJSON(json_ser['geom'])
        lat, lng = geo_json['coordinates']
        del json_ser['geom']
        json_ser['lat'] = lat
        json_ser['lng'] = lng
        return json_ser

    @classmethod
    def read(cls, sid: int):
        return cls.query \
            .filter(Store.sid == sid) \
            .filter(Store.enable == True) \
            .first()

    @classmethod
    def read_list(cls, lat: float, lng: float, name: str, radius: float = 5.0, page: int = 1, page_size: int = 50):

        radius = max(radius, 5)
        radius = min(radius, 20)

        store_list = cls.query \
            .filter(ST_Distance(Store.geom, 'POINT({lat} {lng})'.format(lat=lat, lng=lng)) <= radius)

        if name:
            store_lit = store_lit.filter(Store.name.like('%' + name + '%'))

        store_list = store_list.offset((page-1)*page_size).limit(page_size)

        return store_list.all()
