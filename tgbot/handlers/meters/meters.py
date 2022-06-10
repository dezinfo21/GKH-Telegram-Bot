""" Meters module """
from typing import NoReturn

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import html_decoration as mrd

from tgbot.keyboards.default import main_kb
from tgbot.keyboards.inline import get_meters_kb
from tgbot.services.database import get_user_decorator, UserModel
from tgbot.services.database import set_user_remind_send_meters
from tgbot.states import Menus, SendMeters
from tgbot.utils.language import get_strings_sync, get_strings_decorator, Strings


@get_user_decorator
@get_strings_decorator(module="contact_info")
async def choose_meters(message: Message, user: UserModel, strings: Strings, state: FSMContext):
    """
    Message handler to choose what kind of meters to send

    Args:
        message (aiogram.types.Message):
        user (tgbot.services.database.UserModel):
        strings (tgbot.utils.language.Strings):
        state (aiogram.dispatcher.FSMContext):
    """
    await message.answer(
        mrd.bold(strings.get_strings(mas_name_="STRINGS", module_="buttons")["submit_meters"]),
        reply_markup=main_kb
    )

    if user:
        kb = await get_meters_kb(remind_send_meters=user.rem_send_meters)
    else:
        kb = await get_meters_kb()
    await message.answer(
        strings["choose_meters"],
        reply_markup=kb
    )

    await state.finish()
    await state.set_state(Menus.metersMenu)


@get_user_decorator
@get_strings_decorator(module="remind_send_meters")
async def remind_send_meters(call: CallbackQuery, user: UserModel, strings: Strings):
    """
    Callback query handler to enable and disable send meters notifications

    Args:
        call (aiogram.types.CallbackQuery):
        user (tgbot.services.database.UserModel):
        strings (tgbot.utils.language.Strings):
    """
    if not await set_user_remind_send_meters(user.user_id):
        return await call.answer(strings["fail"])

    if user.rem_send_meters:
        await call.answer(strings["disable"])
    else:
        await call.answer(strings["enable"])

    kb = await get_meters_kb(remind_send_meters=not user.rem_send_meters)
    await call.message.edit_reply_markup(kb)


def register_meters(dp: Dispatcher) -> NoReturn:
    """
    Register handlers for meters

    Args:
        dp (aiogram.Dispatcher):

    Returns:
        NoReturn
    """
    strings = get_strings_sync(module="buttons")

    dp.register_message_handler(
        choose_meters,
        Text(equals=strings["submit_meters"]),
        state=[Menus.verifiedUserMenu, Menus.notVerifiedUserMenu]
    )

    dp.register_message_handler(
        choose_meters,
        Text(equals=strings["back"]),
        state=[SendMeters]
    )

    dp.register_callback_query_handler(
        remind_send_meters,
        Text(equals="remind_send_meters"),
        state=Menus.metersMenu
    )
