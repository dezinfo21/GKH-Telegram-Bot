""" Contact specialist module """
from typing import NoReturn

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery

from tgbot.keyboards.default import back_kb
from tgbot.keyboards.inline import specialists_kb, get_price_list_kb
from tgbot.keyboards.inline.callback_data import specialists_cd
from tgbot.states import Menus, ContactSpecialist
from tgbot.utils.language import get_strings_sync, get_strings_decorator, Strings


@get_strings_decorator(module="buttons")
async def contact_specialist(message: Message, strings: Strings, state: FSMContext):
    """
    Message handler to contact specialist

    Args:
        message (aiogram.types.Message):
        strings (tgbot.utils.language.Strings):
        state (aiogram.dispatcher.FSMContext):
    """
    await message.answer(
        strings["call_specialist"],
        reply_markup=back_kb
    )
    await message.answer(
        strings.get_strings(mas_name_="STRINGS", module_="contact_info")["choose_specialist"],
        reply_markup=specialists_kb
    )

    await state.finish()
    await state.set_state(Menus.specialistsMenu)


@get_strings_decorator(module="buttons")
async def specialist_price_list(
        call: CallbackQuery, strings: Strings, callback_data: dict, state: FSMContext
):
    """
    Callback query handler to get specialist's price list

    Args:
        call (aiogram.types.CallbackQuery):
        strings (tgbot.utils.language.Strings):
        callback_data (aiogram.types.CallbackQuery):
        state (aiogram.dispatcher.FSMContext):
    """
    await call.answer()

    specialist = callback_data["spec"]

    async with state.proxy() as data:
        data["spec"] = specialist

    kb = await get_price_list_kb(specialist)

    await call.message.edit_text(strings[specialist], reply_markup=kb)

    await state.set_state(Menus.servicesMenu)


def register_contact_specialist(dp: Dispatcher) -> NoReturn:
    """
    Register handlers to contact specialist

    Args:
        dp (aiogram.Dispatcher):

    Returns:
        NoReturn
    """
    strings = get_strings_sync(module="buttons")

    dp.register_message_handler(
        contact_specialist,
        Text(equals=strings["call_specialist"]),
        state=Menus.bidsMenu
    )

    dp.register_message_handler(
        contact_specialist,
        Text(equals=strings["back"]),
        state=[Menus.specialistsMenu, Menus.servicesMenu, ContactSpecialist]
    )

    dp.register_callback_query_handler(
        specialist_price_list,
        specialists_cd.filter(),
        state=Menus.specialistsMenu
    )
