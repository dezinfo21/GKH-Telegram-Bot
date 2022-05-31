""" Main menu module """
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message

from tgbot.keyboards.default import get_not_ver_user_kb, get_ver_user_kb
from tgbot.states import Menus


async def main_menu_new(message: Message, state: FSMContext):
    """
    Bot main manu for new users

    Args:
        message (aiogram.types.Message):
        state (aiogram.dispatcher.FSMContext):
    """
    kb = await get_not_ver_user_kb()
    await message.answer("<b>Главное меню</b>", reply_markup=kb)

    await state.finish()
    await state.set_state(Menus.notVerifiedUserMenu)


async def main_menu(message: Message, state: FSMContext):
    """
    Bot main manu for verified users

    Args:
        message (aiogram.types.Message):
        state (aiogram.dispatcher.FSMContext):
    """
    kb = await get_ver_user_kb()
    await message.answer("<b>Главное меню</b>", reply_markup=kb)

    await state.finish()
    await state.set_state(Menus.verifiedUserMenu)


def register_main_menu(dp: Dispatcher):
    dp.register_message_handler(
        main_menu_new,
        Text(equals="Главное меню"),
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
        Text(equals="Главное меню"),
        state="*"
    )
    dp.register_message_handler(
        main_menu,
        commands=["menu"],
        state="*"
    )
