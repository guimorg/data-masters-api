"""Logging for API"""
import sys
import logging

from api import APP_NAME
from api.config import LOGGING_OPTION as config_logging_option


logging.basicConfig(
    stream=sys.stderr,
    level=logging.getLevelName(config_logging_option("level")),
    format="%(asctime)s\t[%(levelname)s]\t%(message)s"
)


def make_logger():
    """
    Factory for Logger.
    Sets up according to basicConfig.
    If any more configuration is needed, this is the place to do it.
    """
    _logger = logging.Logger(name=APP_NAME)

    handler = logging.StreamHandler()
    _logger.addHandler(handler)
    return _logger


def get_logger():
    _logger = logging.getLogger(APP_NAME)

    if isinstance(_logger, logging.RootLogger):
        # Better not to mess with RootLogger
        _logger = make_logger()

    return _logger
