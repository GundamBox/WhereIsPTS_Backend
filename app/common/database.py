import traceback
import logging
from abc import abstractclassmethod

from flask_sqlalchemy import SQLAlchemy

from app.common.exception import FlaskException

db = SQLAlchemy()
log = logging.getLogger(__name__)


class Base(db.Model):
    __abstract__ = True

    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
            log.debug('Create Success')
        except Exception as e:
            log.exception('Something get error', e)
            tb = traceback.format_exc()
            raise FlaskException(message=tb, status_code=500)

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
        except Exception as e:
            log.exception('Something get error', e)
            tb = traceback.format_exc()
            raise FlaskException(message=tb, status_code=500)

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            tb = traceback.format_exc()
            raise FlaskException(message=tb, status_code=500)
