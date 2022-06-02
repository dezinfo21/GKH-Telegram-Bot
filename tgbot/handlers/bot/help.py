""" Bot help module """
from typing import NoReturn

from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.utils.language import get_strings_decorator, Strings


@get_strings_decorator(module="bot_help")
async def bot_help(message: Message, strings: Strings):
    """
    Message handler for help information

    Args:
        message (aiogram.types.Message):
        strings (dict):
    """
    full_name = message.from_user.full_name
    admin_username = strings.get_strings(module_="admin", mas_name_="STRINGS")["username"]

    await message.answer(strings["help"].format(full_name=full_name, admin_username=admin_username))


def register_help(dispatcher: Dispatcher) -> NoReturn:
    """
    Register help handler

    Args:
        dispatcher (aiogram.Dispatcher):

    Returns:
        NoReturn
    """
    dispatcher.register_message_handler(bot_help, commands=["help"], state="*")
