from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import Message

from tgbot.states import Menus


async def bot_news(message: Message):
    await message.answer("Этот раздел еще не готов")


def register_news(dp: Dispatcher):
    dp.register_message_handler(
        bot_news, Text(equals="Новости"), state=[Menus.verifiedUserMenu, Menus.notVerifiedUserMenu]
    )
