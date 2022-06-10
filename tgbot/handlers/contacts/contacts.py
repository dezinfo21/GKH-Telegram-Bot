""" Contacts module """
from typing import NoReturn

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message
from aiogram.utils.markdown import html_decoration as mrd

from tgbot.keyboards.default import contacts_kb
from tgbot.states import Menus, ContactSupport
from tgbot.utils.language import get_strings_decorator, Strings, get_strings_sync


@get_strings_decorator(module="buttons")
async def bot_contacts(message: Message, strings: Strings, state: FSMContext):
    """
    Message handler for contacts
    Args:
        message (aiogram.types.Message):
        strings (tgbot.utils.language.Strings):
        state (aiogram.dispatcher.FSMContext):
    """
    await message.answer(
        mrd.bold(strings["contacts"]),
        reply_markup=contacts_kb
    )

    await state.finish()
    await state.set_state(Menus.contactsMenu)


@get_strings_decorator(module="buttons")
async def get_emergency_contacts(message: Message, strings: Strings):
    """
    Message handler to get emergency contacts

    Args:
        message (aiogram.types.Message):
        strings (tgbot.utils.language.Strings):
    """
    await message.answer(strings["emergency_contacts"])
    await message.answer(
        strings.get_strings(mas_name_="STRINGS", module_="contact_info")["emergency_phone_numbers"]
    )


def register_contacts(dp: Dispatcher) -> NoReturn:
    """
    Register contacts handlers

    Args:
        dp (aiogram.Dispatcher):

    Returns:
        NoReturn
    """
    strings = get_strings_sync(module="buttons")

    dp.register_message_handler(
        bot_contacts,
        Text(equals=strings["contacts"]),
        state=[Menus.notVerifiedUserMenu, Menus.verifiedUserMenu]
    )

    dp.register_message_handler(
        bot_contacts,
        Text(equals=strings["back"]),
        state=[ContactSupport]
    )

    dp.register_message_handler(
        get_emergency_contacts,
        Text(equals=[strings["emergency_contacts"], strings["emergency"]]),
        state=[Menus.contactsMenu, Menus.verifiedUserMenu]
    )
    