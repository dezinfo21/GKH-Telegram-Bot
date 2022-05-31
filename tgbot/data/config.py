from dataclasses import dataclass

from environs import Env


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]
    use_redis: bool


@dataclass
class Channels:
    support: int


@dataclass
class Miscellaneous:
    debug: bool
    default_lang: str


@dataclass
class Config:
    tg_bot: TgBot
    channels: Channels
    misc: Miscellaneous


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ADMINS"))),
            use_redis=env.bool("USE_REDIS"),
        ),
        channels=Channels(
            support=env.int("SUPPORT_CHANNEL_ID")
        ),
        misc=Miscellaneous(
            debug=env.bool("DEBUG"),
            default_lang=env.str("DEFAULT_LANG")
        )
    )
