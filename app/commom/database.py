import logging
from abc import abstractclassmethod

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
log = logging.getLogger(__name__)


class Base(db.Model):
    __abstract__ = True

    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
            log.debug('Create Success')
            return True
        except Exception as e:
            print(e)
            log.exception('Something get wrong', e)
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
            log.debug('Update Success')
            return True
        except Exception as e:
            log.exception('Something get wrong', e)
            return False

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False
