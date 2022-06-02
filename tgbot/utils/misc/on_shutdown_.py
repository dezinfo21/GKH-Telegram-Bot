""" On shutdown """
from typing import NoReturn

from aiogram import Dispatcher


async def on_shutdown(dispatcher: Dispatcher) -> NoReturn:
    """
    After bot stopped

    Args:
        dispatcher ():

    Returns:
        NoReturn
    """
    pass
