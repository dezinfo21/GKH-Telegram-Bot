""" Bot bids module """
from typing import NoReturn

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message
from aiogram.utils.markdown import html_decoration as mrd

from tgbot.keyboards.default import bids_kb
from tgbot.states import Menus, AddBid
from tgbot.utils.language import get_strings_decorator, Strings, get_strings_sync


@get_strings_decorator(module="buttons")
async def add_bid(message: Message, strings: Strings, state: FSMContext):
    """
    Message handler for add bid

    Args:
        message (aiogram.types.Message):
        strings (tgbot.utils.language.Strings):
        state (aiogram.dispatcher.FSMContext):
    """
    await message.answer(
        mrd.bold(strings["add_bid"]),
        reply_markup=bids_kb
    )

    await state.finish()
    await state.set_state(Menus.bidsMenu)


def register_add_bid(dp: Dispatcher) -> NoReturn:
    """
    Register add bid handler

    Args:
        dp (aiogram.Dispatcher):

    Returns:
        NoReturn
    """
    strings = get_strings_sync(module="buttons")

    dp.register_message_handler(
        add_bid,
        Text(equals=strings["add_bid"]),
        verified_only=True,
        state=Menus.verifiedUserMenu,
    )

    dp.register_message_handler(
        add_bid,
        Text(equals=strings["back"]),
        verified_only=True,
        state=[AddBid, Menus.specialistsMenu],
    )
