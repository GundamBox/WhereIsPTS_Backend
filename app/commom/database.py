from abc import abstractclassmethod

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.inspection import inspect

db = SQLAlchemy()


class Base(db.Model):
    __abstract__ = True

    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False

    @abstractclassmethod
    def read(cls, *args, **kwargs):
        raise NotImplementedError

    @abstractclassmethod
    def read_list(cls, *args, **kwargs):
        raise NotImplementedError

    def update(self):
        try:
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False
