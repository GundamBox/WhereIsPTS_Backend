import configparser
import functools
import logging
import time
from logging.handlers import RotatingFileHandler

DEFAULT_LOG_LEVEL = logging.INFO
LOG_FILE_SIZE_LIMIT = 2 * 1024 * 1024
LOG_BACKUP_COUNT = 20


def import_config(config_path: str) -> configparser.ConfigParser:

    config = configparser.ConfigParser()
    config.optionxform = str
    config.read(config_path)

    return config


def export_config(config: configparser.ConfigParser, config_path: str):

    with open(config_path, 'w') as configfile:
        config.write(configfile)


def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")


def get_file_handler(log_file_name: str,
                     log_level: int = DEFAULT_LOG_LEVEL,
                     log_format: str = '%(asctime)s %(levelname)-8s%(filename)s:[%(lineno)d]: %(message)s',
                     log_file_size_limit: int = LOG_FILE_SIZE_LIMIT,
                     log_backup_count: int = LOG_BACKUP_COUNT) -> RotatingFileHandler:

    handler = RotatingFileHandler(log_file_name, mode='a',
                                  maxBytes=log_file_size_limit,
                                  backupCount=log_backup_count,
                                  encoding=None, delay=0)
    formatter = logging.Formatter(log_format)
    handler.setFormatter(formatter)
    handler.setLevel(log_level)

    return handler


def get_console_handler(log_level: int = DEFAULT_LOG_LEVEL,
                        log_format: str = '%(levelname)-8s%(filename)s:[%(lineno)d]: %(message)s') -> logging.StreamHandler:

    handler = logging.StreamHandler()
    formatter = logging.Formatter(log_format)
    handler.setFormatter(formatter)
    handler.setLevel(log_level)

    return handler


def get_logger(logger_name: str = 'root'):
    logger = logging.getLogger(logger_name)
    logger.setLevel(DEFAULT_LOG_LEVEL)

    return logger


logger = get_logger()
