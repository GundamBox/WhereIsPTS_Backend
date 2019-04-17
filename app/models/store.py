import datetime
import math

from sqlalchemy import Sequence
from .base import Serializer, db


class Store(db.Model, Serializer):
    __table__name = 'store'

    id = db.Column(db.Integer, Sequence('store_id_seq'), primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(256), nullable=True)
    news = db.Column(db.String(128), nullable=False)
    switchable = db.Column(db.Boolean, nullable=False)
    lastModified = db.Column(db.DateTime, nullable=False,
                             default=datetime.datetime.now)
    ip = db.Column(db.String(40), nullable=False)

    def __init__(self, name, lat, lng, address, news, switchable, ip):
        self.name = name
        self.lat = lat
        self.lng = lng
        self.address = address
        self.news = news
        self.switchable = switchable
        self.ip = ip

    @classmethod
    def get_by_id(cls, store_id):
        return cls.query.filter(Store.id == store_id).first()

    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def update(self):
        try:
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False

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
