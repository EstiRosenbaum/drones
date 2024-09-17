import logging
from logging.handlers import RotatingFileHandler


def create_logger(logger_name: str) -> logging.Logger:
    FORMAT = "%(asctime)s [%(levelname)s] %(message)s"
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    handler = RotatingFileHandler(
        "/usr/share/filebeat/app.log", maxBytes=10000, backupCount=1
    )
    formatter = logging.Formatter(FORMAT)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


logger = create_logger(__name__)
