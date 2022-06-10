""" Support module """
from typing import List, NoReturn

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery, ContentType

from tgbot.handlers import handlers
from tgbot.keyboards.default import back_kb
from tgbot.services.database import get_user_decorator, UserModel
from tgbot.states import Menus, ContactSupport
from tgbot.utils.language import get_strings_decorator, Strings, get_strings_sync
from tgbot.utils.validators import text_validator


@get_strings_decorator(module="contact_info")
async def contact_support_new(message: Message, strings: Strings, state: FSMContext):
    """
    Message handler to contact support team for not verified users

    Args:
        message (aiogram.types.Message):
        strings (tgbot.utils.language.Strings):
        state (aiogram.dispatcher.FSMContext):
    """
    await message.answer(
        strings.get_strings(mas_name_="STRINGS", module_="buttons")["support"],
        reply_markup=back_kb
    )
    await message.answer(strings["flat_number"])

    await state.set_state(ContactSupport.flatNumber)


@get_user_decorator
@get_strings_decorator(module="contact_info")
async def contact_support(message: Message, user: UserModel, strings: Strings, state: FSMContext):
    """
    Message handler to contact support team for already verified users

    Args:
        message (aiogram.types.Message):
        user (tgbot.services.database.UserModel)
        strings (tgbot.utils.language.Strings):
        state (aiogram.dispatcher.FSMContext):
    """
    await message.answer(
        strings.get_strings(mas_name_="STRINGS", module_="buttons")["support"],
        reply_markup=back_kb
    )

    await message.answer(strings["text_support"])

    async with state.proxy() as data:
        data["flat_number"] = user.flat_number
        data["phone_number"] = user.phone_number
        data["full_name"] = user.full_name

    await state.set_state(ContactSupport.text)


@get_strings_decorator(module="contact_info")
async def contact_form_flat_number(message: Message, strings: Strings, state: FSMContext):
    """
    Message handler for contact's form flat number

    Args:
        message (aiogram.types.Message):
        strings (tgbot.utils.language.Strings):
        state (aiogram.dispatcher.FSMContext):
    """
    await handlers.flat_number_handler(
        message=message,
        state=state,
        next_state=ContactSupport.phoneNumber,
        message_on_success=strings["phone_number"]
    )


@get_strings_decorator(module="contact_info")
async def contact_form_phone_number(message: Message, strings: Strings, state: FSMContext):
    """
    Message handler for contact's form phone number

    Args:
        message (aiogram.types.Message):
        strings (tgbot.utils.language.Strings):
        state (aiogram.dispatcher.FSMContext):
    """
    await handlers.phone_number_handler(
        message=message,
        state=state,
        next_state=ContactSupport.fullName,
        message_on_success=strings["full_name"]
    )


@get_strings_decorator(module="contact_info")
async def contact_form_full_name(message: Message, strings: Strings, state: FSMContext):
    """
    Message handler for contact's form full name

        message (aiogram.types.Message):
        strings (tgbot.utils.language.Strings):
        state (aiogram.dispatcher.FSMContext):
    """
    await handlers.full_name_handler(
        message=message,
        state=state,
        next_state=ContactSupport.text,
        message_on_success=strings["text_support"]
    )


@get_strings_decorator(module="contact_info")
async def contact_form_text(message: Message, strings: Strings, state: FSMContext):
    """
    Message handler for contact's form tex

    Args:
        message (aiogram.types.Message):
        strings (tgbot.utils.language.Strings):
        state (aiogram.dispatcher.FSMContext):
    """
    await handlers.text_handler(
        message=message,
        validator=text_validator,
        state=state,
        next_state=ContactSupport.image,
        message_on_success=strings["img_support"]
    )


@get_user_decorator
@get_strings_decorator(module="support")
async def skip_image(call: CallbackQuery, user: UserModel, strings: Strings, state: FSMContext):
    """
    Callback query handler to skip contact's form image

    Args:
        call (aiogram.types.CallbackQuery):
        user (tgbot.services.database.UserModel):
        strings (tgbot.utils.language.Strings):
        state (aiogram.dispatcher.FSMContext):
    """
    await handlers.skip_image_handler(
        call=call,
        user=user,
        state=state,
        message_on_success=strings["success"],
        message_on_fail=strings["fail"]
    )


@get_user_decorator
@get_strings_decorator(module="support")
async def contact_form_image(message: Message, user: UserModel, strings: Strings, state: FSMContext):
    """
    Message handler for contact's form photo or document

    Args:
        message (aiogram.types.Message):
        user (tgbot.services.database.UserModel):
        strings (tgbot.utils.language.Strings):
        state (aiogram.dispatcher.FSMContext):
    """
    await handlers.image_handler(
        message=message,
        user=user,
        state=state,
        message_on_success=strings["success"],
        message_on_fail=strings["fail"],
        album=[message]
    )


@get_user_decorator
@get_strings_decorator(module="support")
async def contact_form_album(
        message: Message, user: UserModel, strings: Strings, album: List[Message], state: FSMContext
):
    """
    Message handler for contact's form album of photos and documents

    Args:
        message (aiogram.types.Message):
        user (tgbot.services.database.UserModel):
        strings (tgbot.utils.language.Strings):
        album (List[aiogram.types.Message]):
        state (aiogram.dispatcher.FSMContext):
    """
    await handlers.image_handler(
        message=message,
        user=user,
        state=state,
        message_on_success=strings["success"],
        message_on_fail=strings["fail"],
        album=album,
    )


def register_support(dp: Dispatcher) -> NoReturn:
    """
    Register handlers for support contact form

    Args:
        dp (aiogram.Dispatcher):

    Returns:
        NoReturn
    """
    strings = get_strings_sync(module="buttons")

    dp.register_message_handler(
        contact_support_new,
        Text(equals=strings["support"]),
        not_verified_only=True,
        state=Menus.contactsMenu
    )

    dp.register_message_handler(
        contact_support,
        Text(equals=strings["support"]),
        verified_only=True,
        state=[Menus.contactsMenu, Menus.bidsMenu]
    )

    dp.register_message_handler(
        contact_form_flat_number,
        state=ContactSupport.flatNumber
    )

    dp.register_message_handler(
        contact_form_phone_number,
        state=ContactSupport.phoneNumber
    )

    dp.register_message_handler(
        contact_form_full_name,
        state=ContactSupport.fullName
    )

    dp.register_message_handler(
        contact_form_text,
        state=ContactSupport.text
    )

    dp.register_callback_query_handler(
        skip_image,
        Text(equals="skip"),
        state=ContactSupport.image
    )

    dp.register_message_handler(
        contact_form_image,
        is_media_group=False,
        content_types=[ContentType.PHOTO, ContentType.DOCUMENT],
        state=ContactSupport.image
    )

    dp.register_message_handler(
        contact_form_album,
        is_media_group=True,
        content_types=[ContentType.PHOTO, ContentType.DOCUMENT],
        state=ContactSupport.image
    )
