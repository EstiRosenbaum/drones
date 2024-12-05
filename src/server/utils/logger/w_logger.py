import logging
import os
from datetime import date
from logging.handlers import RotatingFileHandler


def create_logger(logger_name: str) -> logging.Logger:
    FORMAT = 'time="%(asctime)s" level="%(levelname)s" source="%(module)s.%(funcName)s:%(lineno)d" thread=%(thread)d message="%(message)s"'
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    handler = RotatingFileHandler(
        f"{os.path.dirname(__file__)}/{date.today()}.log", maxBytes=4096, backupCount=3
    )
    formatter = logging.Formatter(FORMAT)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


logger = create_logger(__name__)
