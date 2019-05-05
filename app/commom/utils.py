import logging
import traceback

from flask import current_app

from app.models import Log


def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")


class SQLAlchemyHandler(logging.Handler):

    def emit(self, record):
        trace = None
        exc = record.__dict__['exc_info']
        if exc:
            trace = traceback.format_exc()
        log = Log(
            logger=record.__dict__['name'],
            level=record.__dict__['levelname'],
            trace=trace,
            msg=record.__dict__['msg'],)
        current_app._get_current_object().db.session.add(log)
        current_app._get_current_object().db.session.commit()
