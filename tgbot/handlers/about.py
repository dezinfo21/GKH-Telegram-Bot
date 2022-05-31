""" Bot about module """
from typing import NoReturn

from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import Message

from tgbot.states import Menus
from tgbot.utils.language import get_strings_decorator, Strings


@get_strings_decorator(module="bot_about")
async def bot_about(message: Message, strings: Strings):
    """
    Bot /about command

    Args:
        message (aiogram.types.Message):
        strings (tgbot.utils.language.Strings):
    """
    await message.answer(strings["about"])


def register_about(dispatcher: Dispatcher) -> NoReturn:
    """
    Register bot_about handler

    Args:
        dispatcher (aiogram.Dispatcher):

    Returns:
        NoReturn
    """
    dispatcher.register_message_handler(
        bot_about,
        Text(equals="О боте"),
        state=[Menus.verifiedUserMenu, Menus.notVerifiedUserMenu]
    )
    dispatcher.register_message_handler(
        bot_about,
        commands=["about"],
        state=[Menus.verifiedUserMenu, Menus.notVerifiedUserMenu]
    )
