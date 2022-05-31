from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message

from tgbot.keyboards.default import get_contacts_kb
from tgbot.states import Menus


async def bot_contacts(message: Message, state: FSMContext):
    kb = await get_contacts_kb()
    await message.answer("<b>Контакты</b>", reply_markup=kb)

    await state.finish()
    await state.set_state(Menus.contactsMenu)


async def emergency_contacts(message: Message):
    await message.answer("<b>Телефоны Экстренных служб</b>")
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


def register_contacts(dp: Dispatcher):
    dp.register_message_handler(
        bot_contacts,
        Text(equals="Контакты"),
        state=[Menus.notVerifiedUserMenu, Menus.verifiedUserMenu]
    )
    dp.register_message_handler(
        emergency_contacts,
        Text(equals=["Телефоны Экстренных служб", "Сообщить об екстренной ситуации"]),
        state=[Menus.contactsMenu, Menus.verifiedUserMenu]
    )
    