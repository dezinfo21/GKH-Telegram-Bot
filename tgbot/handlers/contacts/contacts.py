""" Contacts module """
from typing import NoReturn

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message
from aiogram.utils.markdown import html_decoration as mrd

from tgbot.keyboards.default import contacts_kb
from tgbot.states import Menus, ContactForm
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
    await message.answer(strings["emerg_contacts"])
    await message.answer(
        "Единый номер экстренных служб: <code>112</code>\n"
        "Пожарная служба: <code>101</code>\n"
        "Полиция: <code>102</code>\n"
        "Скорая помощь: <code>103</code>\n"
        "Служба газа: <code>104</code>\n\n"
        "<b>Памятка при обращении на номер «112»</b>\n"
        "Обращаясь по номеру «112», помните следующее: Номер «112» – это номер телефона, по которому можно позвонить: " 
        "чтобы связаться с какой-либо экстренной оперативной службой; в любой стране ЕС;" 
        "с мобильных или со стационарных телефонов, в том числе общественных таксофонов; круглосуточно и бесплатно." 
        "Звоните на номер «112» только в случаях: если Вы нуждаетесь в экстренной помощи, когда возникла" 
        "реальная угроза жизни, здоровью, имуществу или окружающей среде; или есть причины подозревать это."
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
        Text(equals=[strings["contacts"], strings["back"]]),
        state=[Menus.notVerifiedUserMenu, Menus.verifiedUserMenu, ContactForm]
    )
    dp.register_message_handler(
        get_emergency_contacts,
        Text(equals=[strings["emerg_contacts"], strings["emergency"]]),
        state=[Menus.contactsMenu, Menus.verifiedUserMenu]
    )
    