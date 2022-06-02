""" Logging module """
import logging
import os.path
from logging.handlers import RotatingFileHandler
from typing import NoReturn

from definitions import LOGS_DIR
from tgbot.data.config import load_config

config = load_config(".env")


class _InfoFilter(logging.Filter):
    """
    Filter to catch only INFO logs
    """
    def filter(self, record: logging.LogRecord) -> bool:
        return record.levelno == logging.INFO


def _get_console_handler() -> logging.StreamHandler:
    """
    Configure console handler

    Returns:
        logging.StreamHandler
    """
    handler = logging.StreamHandler()

    handler.setLevel(logging.INFO if config.tg_bot.prod else logging.DEBUG)
    handler.setFormatter(logging.Formatter(config.misc.basic_log_format))

    return handler


def _get_file_handler(filename: str = "logs.log") -> RotatingFileHandler:
    """
    Configure rotating file handler for info logs

    Args:
        filename (str): filename where logs should be saved

    Returns:
        logging.handlers.RotatingFileHandler
    """
    path = os.path.join(LOGS_DIR, filename)

    handler = RotatingFileHandler(
        filename=path,
        maxBytes=10485760,
        backupCount=1
    )

    handler.addFilter(_InfoFilter())
    handler.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter(config.misc.standard_log_format))

    return handler


def _get_errors_file_handler(filename: str = "errors.log") -> RotatingFileHandler:
    """
    Configure rotating file handler for error logs

    Args:
        filename (str): filename where logs should be saved

    Returns:
        logging.handlers.RotatingFileHandler
    """
    path = os.path.join(LOGS_DIR, filename)

    handler = RotatingFileHandler(
        filename=path,
        maxBytes=10485760,
        backupCount=1,
    )

    handler.setLevel(logging.WARNING)
    handler.setFormatter(logging.Formatter(config.misc.standard_log_format))

    return handler


def setup() -> NoReturn:
    """
    Setup logging module

    Returns:
        NoReturn
    """
    logging.basicConfig(
        format=config.misc.basic_log_format,
        level=logging.DEBUG,
        handlers=[
            _get_console_handler(),
            _get_file_handler(),
            _get_errors_file_handler()
        ] if config.tg_bot.prod else [
            _get_console_handler()
        ]
    )
