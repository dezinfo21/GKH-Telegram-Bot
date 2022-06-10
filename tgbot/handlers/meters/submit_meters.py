""" Submit meters reinder module """
import logging
from typing import List, NoReturn

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery, ContentType

from tgbot.data.config import load_config
from tgbot.handlers import handlers
from tgbot.keyboards.default import back_kb
from tgbot.keyboards.inline.callback_data import meters_cd
from tgbot.services.database import get_user_decorator, UserModel
from tgbot.states import Menus, SendMeters
from tgbot.utils.language import get_strings_decorator, Strings
from tgbot.utils.validators import meters_validator

config = load_config(".env")
log = logging.getLogger("prod" if config.tg_bot.prod else "dev")


@get_strings_decorator(module="contact_info")
async def submit_meters_new(
        call: CallbackQuery, strings: Strings, callback_data: dict, state: FSMContext
):
    """
    Callback query handler to submit meters from new users

    Args:
        call (aiogram.types.CallbackQuery):
        strings (tgbot.utils.language.Strings):
        callback_data (dict)
        state (aiogram.dispatcher.FSMContext):
    """
    await call.answer()

    await call.message.answer(
        strings["text_send_meters"],
        reply_markup=back_kb
    )

    async with state.proxy() as data:
        data["meters_type"] = callback_data["type_"]

    await state.set_state(SendMeters.flatNumber)


@get_user_decorator
@get_strings_decorator(module="contact_info")
async def submit_meters(
        call: CallbackQuery, user: UserModel, strings: Strings, callback_data: dict, state: FSMContext
):
    """
    Callback query handler to submit meters from already verified user

    Args:
        call (aiogram.types.CallbackQuery):
        user (tgbot.services.database.UserModel):
        strings (tgbot.utils.language.Strings):
        callback_data (dict)
        state (aiogram.dispatcher.FSMContext):
    """
    await call.answer()

    await call.message.answer(
        strings["text_send_meters"],
        reply_markup=back_kb
    )

    async with state.proxy() as data:
        data["meters_type"] = callback_data["type_"]
        data["flat_number"] = user.flat_number

    await state.set_state(SendMeters.text)


@get_strings_decorator(module="contact_info")
async def meters_flat_number(message: Message, strings: Strings, state: FSMContext):
    """
    Message handler to get flat number for meters from user

    Args:
        message (aiogram.types.Message):
        strings (tgbot.utils.language.Strings):
        state (aiogram.dispatcher.FSMContext):
    """
    await handlers.flat_number_handler(
        message=message,
        state=state,
        next_state=SendMeters.text,
        message_on_success=strings["text_send_meters"]
    )


@get_strings_decorator(module="contact_info")
async def meters_text(message: Message, strings: Strings, state: FSMContext):
    """
    Message handler to get text for meters from user

    Args:
        message (aiogram.types.Message):
        strings (tgbot.utils.language.Strings):
        state (aiogram.dispatcher.FSMContext):
    """
    await handlers.text_handler(
        message=message,
        validator=meters_validator,
        state=state,
        next_state=SendMeters.image,
        message_on_success=strings["img_send_meters"]
    )


@get_user_decorator
@get_strings_decorator(module="send_meters")
async def skip_image(call: CallbackQuery, user: UserModel, strings: Strings, state: FSMContext):
    """
    Callback query handler to skip meters image

    Args:
        call (aiogram.types.CallbackQuery):
        user (tgbot.services.database.UserModel):
        strings (tgbot.utils.language.Strings):
        state (aiogram.dispatcher.FSMContext):
    """
    async with state.proxy() as data:
        meters_type = data["meters_type"]
        data["additional_info"] = strings.get_strings(mas_name_="STRINGS", module_="meters_types")[meters_type]

    await handlers.skip_image_handler(
        call=call,
        user=user,
        state=state,
        message_on_success=strings["success"],
        message_on_fail=strings["fail"]
    )


@get_user_decorator
@get_strings_decorator(module="send_meters")
async def contact_form_image(message: Message, user: UserModel, strings: Strings, state: FSMContext):
    """
    Message handler to get image or document for meters from user

    Args:
        message (aiogram.types.Message):
        user (tgbot.services.database.UserModel):
        strings (tgbot.utils.language.Strings):
        state (aiogram.dispatcher.FSMContext):
    """
    async with state.proxy() as data:
        meters_type = data["meters_type"]
        data["additional_info"] = strings.get_strings(mas_name_="STRINGS", module_="meters_types")[meters_type]

    await handlers.image_handler(
        message=message,
        user=user,
        state=state,
        message_on_success=strings["success"],
        message_on_fail=strings["fail"],
        album=[message]
    )


@get_user_decorator
@get_strings_decorator(module="send_meters")
async def contact_form_album(
        message: Message, user: UserModel, strings: Strings, album: List[Message], state: FSMContext
):
    """
    Message handler to get album(images or documents) for meters from user

    Args:
        message (aiogram.types.Message):
        user (tgbot.services.database.UserModel):
        strings (tgbot.utils.language.Strings):
        album (List[aiogram.types.Message]):
        state (aiogram.dispatcher.FSMContext):
    """
    async with state.proxy() as data:
        meters_type = data["meters_type"]
        data["additional_info"] = strings.get_strings(mas_name_="STRINGS", module_="meters_types")[meters_type]

    await handlers.image_handler(
        message=message,
        user=user,
        state=state,
        message_on_success=strings["success"],
        message_on_fail=strings["fail"],
        album=album
    )


def register_submit_meters(dp: Dispatcher) -> NoReturn:
    """
    Register handlers to submit meters
    Args:
        dp (aiogram.Dispatcher):

    Returns:
        NoReturn
    """
    dp.register_callback_query_handler(
        submit_meters_new,
        meters_cd.filter(),
        not_verified_only=True,
        state=Menus.metersMenu
    )

    dp.register_callback_query_handler(
        submit_meters,
        meters_cd.filter(),
        verified_only=True,
        state=Menus.metersMenu
    )

    dp.register_message_handler(
        meters_flat_number,
        state=SendMeters.flatNumber
    )

    dp.register_message_handler(
        meters_text,
        state=SendMeters.text
    )


    dp.register_callback_query_handler(
        skip_image,
        Text(equals="skip"),
        state=SendMeters.image
    )

    dp.register_message_handler(
        contact_form_image,
        is_media_group=False,
        content_types=[ContentType.PHOTO, ContentType.DOCUMENT],
        state=SendMeters.image
    )

    dp.register_message_handler(
        contact_form_album,
        is_media_group=True,
        content_types=[ContentType.PHOTO, ContentType.DOCUMENT],
        state=SendMeters.image
    )
