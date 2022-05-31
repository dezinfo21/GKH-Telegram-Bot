from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import Message

from tgbot.states import Menus


async def send_meters(message: Message):
    await message.answer("Этот раздел еще не готов.")


def register_send_meters(dp: Dispatcher):
    dp.register_message_handler(
        send_meters, Text(equals="Подать показания счетчика"), state=[Menus.verifiedUserMenu, Menus.notVerifiedUserMenu]
    )
