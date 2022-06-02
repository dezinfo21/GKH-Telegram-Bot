""" Configuration file for bot """
from dataclasses import dataclass
from typing import NoReturn

from environs import Env


@dataclass
class TgBot:
    """
    Bot settings

    Attributes:
        token (str): bot token
        admin_ids (list[int]): list of admins ids
        production (bool): boot in production or not
        use_redis (bool): whether use redis storage or not
    """
    token: str
    admin_ids: list[int]
    prod: bool
    use_redis: bool


@dataclass
class Channels:
    """
    Channels ids

    Attributes:
        support (int): support channel id
    """
    support: int


@dataclass
class Miscellaneous:
    """
    Miscellaneous settings

    Attributes:
        default_lang (str): default language for bot strings
        basic_log_format (str):
        standard_log_format (str):
    """
    default_lang: str
    basic_log_format: str
    standard_log_format: str


@dataclass
class Config:
    """
    Config class

    Attributes:
        tg_bot (TgBot):
        channels: (Channels):
        misc (Miscellaneous):
    """
    tg_bot: TgBot
    channels: Channels
    misc: Miscellaneous


def load_config(path: str = None) -> NoReturn:
    """
    Load bot config file from environment file

    Args:
        path (str): path to environment file

    Returns:
        NoReturn
    """
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ADMINS"))),
            prod=env.bool("PRODUCTION"),
            use_redis=env.bool("USE_REDIS"),
        ),
        channels=Channels(
            support=env.int("SUPPORT_CHANNEL_ID")
        ),
        misc=Miscellaneous(
            default_lang=env.str("DEFAULT_LANG"),
            basic_log_format=env.str("BASIC_LOG_FORMAT"),
            standard_log_format=env.str("STANDARD_LOG_FORMAT")
        )
    )
