""" Bot echo module """
from typing import NoReturn

from aiogram import types, Dispatcher


async def bot_echo_all(*args, **kwargs):
    """ Echo message handler to prevent any random messages from the user """


def register_echo(dp: Dispatcher) -> NoReturn:
    """
    Register echo handler

    Args:
        dp (aiogram.Dispatcher):

    Returns:
        NoReturn
    """
    dp.register_message_handler(bot_echo_all, state="*", content_types=types.ContentTypes.ANY)
