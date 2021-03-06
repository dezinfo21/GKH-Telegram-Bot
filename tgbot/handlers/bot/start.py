""" Bot start module"""
from typing import NoReturn

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.keyboards.default import not_verified_user_kb, verified_user_kb
from tgbot.states import Menus
from tgbot.utils.language import get_strings_decorator, Strings


@get_strings_decorator(module="bot_start")
async def bot_start_new(message: Message, strings: Strings, state: FSMContext):
    """
    Message handler for start command from new users

    Args:
        message (aiogram.types.Message):
        state (aiogram.dispatcher.FSMContext):
        strings (tgbot.utils.language.Strings):
    """
    full_name = message.from_user.full_name

    await message.answer("<b>Главное меню</b>")
    await message.answer(strings["start_new"].format(full_name=full_name), reply_markup=not_verified_user_kb)

    await state.set_state(Menus.notVerifiedUserMenu)


@get_strings_decorator(module="bot_start")
async def bot_start(message: Message, strings: Strings, state: FSMContext):
    """
   Message handler for start command from already verified users

    Args:
        message (aiogram.types.Message):
        state (aiogram.dispatcher.FSMContext):
        strings (tgbot.utils.language.Strings):
    """
    await message.answer("<b>Главное меню</b>")
    await message.answer(strings["start"], reply_markup=verified_user_kb)

    await state.set_state(Menus.verifiedUserMenu)


def register_start(dispatcher: Dispatcher) -> NoReturn:
    """
    Register start handlers

    Args:
        dispatcher (aiogram.Dispatcher):

    Returns:
        NoReturn
    """
    dispatcher.register_message_handler(
        bot_start_new,
        not_verified_only=True,
        commands=["start"],
        state="*"
    )
    dispatcher.register_message_handler(
        bot_start,
        verified_only=True,
        commands=["start"],
        state="*"
    )
