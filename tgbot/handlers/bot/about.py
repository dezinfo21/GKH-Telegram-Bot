""" Bot about module """
from typing import NoReturn

from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import Message

from tgbot.states import Menus
from tgbot.utils.language import get_strings_decorator, Strings, get_strings_sync


@get_strings_decorator(module="bot_about")
async def bot_about(message: Message, strings: Strings):
    """
    Message handler for bot about information

    Args:
        message (aiogram.types.Message):
        strings (tgbot.utils.language.Strings):
    """
    await message.answer(strings["about"])


def register_about(dispatcher: Dispatcher) -> NoReturn:
    """
    Register about handler

    Args:
        dispatcher (aiogram.Dispatcher):

    Returns:
        NoReturn
    """
    strings = get_strings_sync(module="buttons")

    dispatcher.register_message_handler(
        bot_about,
        Text(equals=strings["about"]),
        state=[Menus.verifiedUserMenu, Menus.notVerifiedUserMenu]
    )
    dispatcher.register_message_handler(
        bot_about,
        commands=["about"],
        state=[Menus.verifiedUserMenu, Menus.notVerifiedUserMenu]
    )
