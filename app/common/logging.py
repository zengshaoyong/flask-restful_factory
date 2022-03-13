import logging
from flask.logging import default_handler
from logging.handlers import RotatingFileHandler
from logging import StreamHandler
from flask_limiter.util import get_remote_address
from flask_login import current_user

LOG_PATH = 'logs/flask.log'

LOG_FILE_MAX_BYTES = 100 * 1024 * 1024
LOG_FILE_BACKUP_COUNT = 10


def customer_para():
    if hasattr(current_user, 'id'):
        return {'clientip': get_remote_address(), 'user': current_user.id}
    else:
        return {'clientip': get_remote_address(), 'user': 'anonymous'}


class MyLogger(logging.Logger):
    def makeRecord(self, name, level, fn, lno, msg, args, exc_info, func=None, extra=None, sinfo=None):
        extra = customer_para()
        return super().makeRecord(name, level, fn, lno, msg, args, exc_info, func, extra=extra, sinfo=sinfo)


class Logger(object):
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG)
        logging.setLoggerClass(MyLogger)

    @staticmethod
    def init_app(app):
        app.logger.removeHandler(default_handler)

        formatter = logging.Formatter(
            '%(asctime)s.%(msecs)d %(levelname)s %(filename)s[%(lineno)d] %(clientip)s %(user)s - %(message)s',
            datefmt="%Y-%m-%d %X"
        )

        file_handler = RotatingFileHandler(
            filename=LOG_PATH,
            mode='a',
            maxBytes=LOG_FILE_MAX_BYTES,
            backupCount=LOG_FILE_BACKUP_COUNT,
            encoding='utf-8'
        )

        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)

        stream_handler = StreamHandler()
        stream_handler.setFormatter(formatter)
        stream_handler.setLevel(logging.INFO)

        app.logger.addHandler(file_handler)
        app.logger.addHandler(stream_handler)
