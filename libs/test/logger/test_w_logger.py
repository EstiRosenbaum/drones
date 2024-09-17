import logging

from helpers.logger.w_logger import create_logger


def test_create_logger(logger_name):
    logger = create_logger(logger_name)

    assert isinstance(logger, logging.Logger)
    assert logger.name == logger_name
    handlers = logger.handlers
    has_rotating_handler = any(
        isinstance(handler, logging.handlers.RotatingFileHandler)
        for handler in handlers
    )
    assert has_rotating_handler
