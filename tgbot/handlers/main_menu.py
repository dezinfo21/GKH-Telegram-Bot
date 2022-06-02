""" Main menu module """
from typing import NoReturn

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message
from aiogram.utils.markdown import html_decoration as mrd

from tgbot.keyboards.default import not_verified_user_kb, verified_user_kb
from tgbot.states import Menus
from tgbot.utils.language import get_strings_decorator, Strings, get_strings_sync


@get_strings_decorator(module="buttons")
async def main_menu_new(message: Message, strings: Strings, state: FSMContext):
    """
    Message handler for new users' main menu

    Args:
        message (aiogram.types.Message):
        strings (tgbot.utils.language.Strings):
        state (aiogram.dispatcher.FSMContext):
    """
    await message.answer(
        mrd.bold(strings["main_menu"]),
        reply_markup=not_verified_user_kb
    )

    await state.finish()
    await state.set_state(Menus.notVerifiedUserMenu)


@get_strings_decorator(module="buttons")
async def main_menu(message: Message, strings: Strings, state: FSMContext):
    """
    Message handler for verified users' main menu

    Args:
        message (aiogram.types.Message):
        strings (tgbot.utils.language.Strings):
        state (aiogram.dispatcher.FSMContext):
    """
    await message.answer(
        mrd.bold(strings["main_menu"]),
        reply_markup=verified_user_kb
    )

    await state.finish()
    await state.set_state(Menus.verifiedUserMenu)


def register_main_menu(dp: Dispatcher) -> NoReturn:
    """
    Register main menus handlers

    Args:
        dp (aiogram.Dispatcher):

    Returns:
        NoReturn
    """
    strings = get_strings_sync(module="buttons"
                               )
    dp.register_message_handler(
        main_menu_new,
        Text(equals=strings["main_menu"]),
        not_verified_only=True,
        state="*"
    )
    dp.register_message_handler(
        main_menu_new,
        commands=["menu"],
        not_verified_only=True,
        state="*"
    )
    dp.register_message_handler(
        main_menu,
        Text(equals=strings["main_menu"]),
        state="*"
    )
    dp.register_message_handler(
        main_menu,
        commands=["menu"],
        state="*"
    )
