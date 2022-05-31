from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import Message

from tgbot.states import Menus


async def call_specialist(message: Message):
    await message.answer("Этот раздел еще не готов.")


def register_call_specialist(dp: Dispatcher):
    dp.register_message_handler(
        call_specialist, Text(equals="Заказать справку"), state=Menus.bidsMenu
    )
