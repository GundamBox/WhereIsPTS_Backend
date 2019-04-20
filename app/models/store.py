import datetime
import math

from sqlalchemy import Sequence

from app.commom.database import Base, Serializer, db


class Store(Base, Serializer):
    __table__name = 'store'

    id = db.Column(db.Integer,
                   Sequence('store_id_seq'),
                   primary_key=True)
    name = db.Column(db.String(128),
                     nullable=False)
    lat = db.Column(db.Float,
                    nullable=False)
    lng = db.Column(db.Float,
                    nullable=False)
    address = db.Column(db.String(256),
                        nullable=True)
    switchable = db.Column(db.Boolean,
                           nullable=False)
    enable = db.Column(db.Boolean,
                       nullable=False,
                       default=True)
    disable_vote = db.Column(db.Integer,
                             nullable=False,
                             default=0)
    last_modified = db.Column(db.DateTime,
                              nullable=False,
                              default=datetime.datetime.now)
    last_ip = db.Column(db.String(40), nullable=False)

    def __init__(self, name, lat, lng, address, switchable, ip):
        self.name = name
        self.lat = lat
        self.lng = lng
        self.address = address
        self.switchable = switchable
        self.ip = ip

    @classmethod
    def get_by_id(cls, store_id):
        return cls.query.filter(Store.id == store_id).first()

    @classmethod
    def calc_distance(cls, lat1, lon1, lat2, lon2):
        Earth_radius_km = 6371.009
        km_per_deg_lat = 2 * math.pi * Earth_radius_km / 360.0
        km_per_deg_lon = km_per_deg_lat * math.cos(math.radians(lat1))
        return math.sqrt((km_per_deg_lat * (lat1 - lat2)) ** 2 + (km_per_deg_lon * (lon1 - lon2)) ** 2)

    @classmethod
    def search_by_name(cls, name):
        return cls.query.filter(Store.name.like("%%{name}%%".format(name=name))).all()

    @classmethod
    def search_by_lat_lng(cls, lat: float, lng: float, distance: float):
        store_list = cls.query.all()
        store_list = [store for store in store_list if cls.calc_distance(lat, lng,
                                                                         store.lat, store.lng) < distance]
        return store_list
