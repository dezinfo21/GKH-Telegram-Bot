""" On startup """
import asyncio
import logging
from contextlib import suppress
from typing import NoReturn

from aiogram import Dispatcher, types
from aiogram.utils.exceptions import TelegramAPIError

from tgbot.data.config import load_config
from tgbot.utils.language import get_strings_decorator, Strings

config = load_config(".env")
log = logging.getLogger(__name__)


async def on_startup_notify(dispatcher: Dispatcher)-> NoReturn:
    """
    Notify admins bout bot start

    Args:
        dispatcher (aiogram.Dispatcher):

    Returns:
        NoReturn
    """
    for admin in config.tg_bot.admin_ids:
        with suppress(TelegramAPIError):
            await dispatcher.bot.send_message(
                chat_id=admin, text="Бот успешно запущен", disable_notification=True
            )
            log.info(f"Админ {admin} уведомлен о запуске бота.")
        await asyncio.sleep(0.2)


@get_strings_decorator(module="commands")
async def set_default_commands(dp: Dispatcher, strings: Strings):
    """
    Set default commands for bot

    Args:
        dp (aiogram.Dispatcher):
        strings (tgbot.utils.language.Strings):

    Returns:
        Any | None
    """
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", strings["start"]),
            types.BotCommand("menu", strings["menu"]),
            types.BotCommand("help", strings["help"]),
            types.BotCommand("about", strings["about"])
        ]
    )


async def on_startup(dp: Dispatcher) -> NoReturn:
    """
    Before bot started

    Args:
        dp ():

    Returns:
        NoReturn
    """
    await on_startup_notify(dp)
    await set_default_commands(dp)
