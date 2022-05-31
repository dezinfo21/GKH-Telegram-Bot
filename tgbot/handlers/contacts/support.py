from typing import List

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery, ContentType

from tgbot.keyboards.default import get_main_kb, get_contacts_kb
from tgbot.states import Menus, ContactForm
from tgbot.utils import database, handlers


async def contact_support_new(message: Message, state: FSMContext):
    kb = await get_main_kb()
    await message.answer("<b>Обращение к Руководителю</b>", reply_markup=kb)

    await message.answer("<b>Укажите номер квартиры</b>")

    await state.set_state(ContactForm.flatNumber)


async def contact_support(message: Message, user: database.UserModel, state: FSMContext):
    kb = await get_main_kb()
    await message.answer("<b>Обращение к Руководителю</b>", reply_markup=kb)

    await message.answer("<b>Отправьте текст вашего обращения</b>")

    async with state.proxy() as data:
        data["flat_number"] = user.flat_number
        data["phone_number"] = user.phone_number
        data["full_name"] = user.full_name

    await state.set_state(ContactForm.text)


async def contact_form_flat_number(message: Message, state: FSMContext):
    await handlers.flat_number_handler(
        message=message,
        state=state,
        state_on_success=ContactForm.phoneNumber,
        message_on_success="<b>Введите номер телефона по которому с вами можно связаться, в формате 7 999 999 99 99</b>"
    )


async def contact_form_phone_number(message: Message, state: FSMContext):
    await handlers.phone_number_handler(
        message=message,
        state=state,
        state_on_success=ContactForm.fullName,
        message_on_success="<b>Укажите ваши ФИО</b>"
    )


async def contact_form_full_name(message: Message, state: FSMContext):
    await handlers.full_name_handler(
        message=message,
        state=state,
        state_on_success=ContactForm.text,
        message_on_success="<b>Укажите текст вашего обращения</b>"
    )


async def contact_form_text(message: Message, state: FSMContext):
    await handlers.text_handler(
        message=message,
        state=state,
        state_on_success=ContactForm.image,
        message_on_success="<b>Если требуеться, приложите фотографии к вашему обращению</b>"
    )


async def skip_image(call: CallbackQuery, state: FSMContext):
    await handlers.skip_image_handler(
        call=call,
        state=state,
        state_on_success=Menus.contactsMenu,
        message_on_success="Ваше обращение к руковадителю ЖКХ было успешно отправленно. Ожидайте скорого ответа.",
        keyboard=contacts_kb
    )


async def contact_form_image(message: Message, state: FSMContext):
    await handlers.image_handler(
        message=message,
        state=state,
        state_on_success=Menus.contactsMenu,
        message_on_success="Ваше обращение к руковадителю ЖКХ было успешно отправленно. Ожидайте скорого ответа.",
        keyboard=contacts_kb
    )


async def contact_form_album(message: Message, album: List[Message], state: FSMContext):
    await handlers.album_handler(
        message=message,
        album=album,
        state=state,
        state_on_success=Menus.contactsMenu,
        message_on_success="Ваше обращение к руковадителю ЖКХ было успешно отправленно. Ожидайте скорого ответа.",
        keyboard=contacts_kb
    )


def register_support(dp: Dispatcher):
    dp.register_message_handler(
        contact_support_new,
        Text(equals="Обращение к Руководителю"),
        not_verified_only=True,
        state=Menus.contactsMenu
    )
    dp.register_message_handler(
        contact_support,
        Text(equals="Обращение к Руководителю"),
        verified_only=True,
        state=[Menus.contactsMenu, Menus.bidsMenu]
    )
    dp.register_message_handler(
        contact_form_flat_number,
        state=ContactForm.flatNumber
    )
    dp.register_message_handler(
        contact_form_phone_number,
        state=ContactForm.phoneNumber
    )
    dp.register_message_handler(
        contact_form_full_name,
        state=ContactForm.fullName
    )
    dp.register_message_handler(
        contact_form_text,
        state=ContactForm.text
    )
    dp.register_callback_query_handler(
        skip_image,
        Text(equals="skip"),
        state=ContactForm.image
    )
    dp.register_message_handler(
        contact_form_image,
        is_media_group=False,
        content_types=[ContentType.PHOTO, ContentType.DOCUMENT],
        state=ContactForm.image
    )
    dp.register_message_handler(
        contact_form_album,
        is_media_group=True,
        content_types=[ContentType.PHOTO, ContentType.DOCUMENT],
        state=ContactForm.image
    )
