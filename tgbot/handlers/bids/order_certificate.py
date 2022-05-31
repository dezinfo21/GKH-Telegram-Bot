from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import Message

from tgbot.states import Menus


async def order_certificate(message: Message):
    await message.answer("Этот раздел еще не готов.")


def register_order_certificate(dp: Dispatcher):
    dp.register_message_handler(
        order_certificate, Text(equals="Заказать справку"), state=Menus.bidsMenu
    )
