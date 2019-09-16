"""Configuration for API"""
import pathlib

from configparser import ConfigParser
from functools import (
    partial, lru_cache
)


# Make will put configuration file for us in the correct path
CONFIG_DIR = ".config"
CONFIG_FILE_NAME = "api.conf"
CONFIG_FILE_PATH = pathlib.Path.home() / CONFIG_DIR / CONFIG_FILE_NAME


@lru_cache()
def get_config(path=CONFIG_FILE_PATH):
    """
    Parsing configuration file at ~/.config/api.conf

    Using lru_cache to cache config file and prevent expensive
    I/O tasks.
    """
    config = ConfigParser()
    config.read(path)
    return config


def get_option(section, option, path=CONFIG_FILE_PATH):
    """
    Getting a section from the config file.
    """
    config = get_config(path)
    return config.get(section, option)


SERVER_OPTION = partial(get_option, "server")
LOGGING_OPTION = partial(get_option, "logging")
MACHINE_LEARNING_OPTION = partial(get_option, "model")
WORKERS_OPTION = partial(get_option, "workers")
