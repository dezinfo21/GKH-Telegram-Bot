import logging
from typing import NoReturn

from tgbot.data.config import load_config

_log_format = f"%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"

config = load_config(".env")


def setup() -> NoReturn:
    logging.basicConfig(
        format=_log_format,
        level=logging.DEBUG if config.misc.debug else logging.INFO
    )
