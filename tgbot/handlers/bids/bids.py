from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message

from tgbot.keyboards.default import bids_kb
from tgbot.states import Menus, Bid


async def add_bid(message: Message, state: FSMContext):
    await message.answer("<b>Добавить заявку</b>", reply_markup=bids_kb)

    await state.set_state(Menus.bidsMenu)


def register_add_bid(dp: Dispatcher):
    dp.register_message_handler(
        add_bid,
        Text(equals="Добавить заявку"),
        verified_only=True,
        state=Menus.verifiedUserMenu
    )
