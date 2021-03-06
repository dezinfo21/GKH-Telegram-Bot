""" Basic handlers """
import logging
import re
from typing import List

import pytz
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, MediaGroup
from aiogram.utils.exceptions import ChatNotFound
from aiogram.utils.markdown import html_decoration as mrd

from tgbot.data.config import load_config
from tgbot.keyboards.default import not_verified_user_kb, verified_user_kb
from tgbot.services.database import UserModel
from tgbot.states import Menus
from tgbot.utils.language import get_strings_decorator, Strings
from tgbot.utils.validators import flat_number_validator, phone_number_validator, full_name_validator, AbstractValidator

config = load_config(".env")
log = logging.getLogger("prod" if config.tg_bot.prod else "dev")


async def format_message_to_support(
        additional_info: str | None,
        flat_number: int | None,
        phone_number: int | None,
        full_name: str | None,
        date: str | None,
        text: str | None
) -> str:
    """
    Format a contact information string

    Args:
        additional_info (str):
        flat_number (int):
        phone_number (int):
        full_name (str):
        date (str):
        text (str):

    Returns:
        str: formatted contact information
    """
    caption = ""

    if additional_info is not None:
        caption += f"{additional_info}\n\n"
    if full_name is not None:
        caption += f"<b>ФИО</b>: {full_name}\n"
    if phone_number is not None:
        caption += f"<b>Контактный номер телефона</b>: +{phone_number}\n"
    if flat_number is not None:
        caption += f"<b>Квартира</b>: {flat_number}\n"
    if date is not None:
        caption += f"<b>Дата</b>: {date}\n\n"
    if text is not None:
        caption += text

    return caption


async def flat_number_handler(
        message: Message,
        state: FSMContext,
        next_state: str,
        message_on_success: str
):
    """
    Message handler for flat number

    Args:
        message (aiogram.types.Message): message from user
        state (aiogram.dispatcher.FSMContext): current state
        next_state (aiogram.dispatcher.filters.state.State): next state to set
        message_on_success (str): message to send to user if validation succeed
    """
    flat_number_str = message.text

    if not await flat_number_validator.validate(flat_number_str):
        return await message.answer(flat_number_validator.valid_format)

    async with state.proxy() as data:
        data["flat_number"] = int(flat_number_str)

    await message.answer(message_on_success)

    await state.set_state(next_state)


async def phone_number_handler(
        message: Message,
        state: FSMContext,
        next_state: str,
        message_on_success: str
):
    """
    Message handler for phone number

    Args:
        message (aiogram.types.Message): message from user
        state (aiogram.dispatcher.FSMContext): current state
        next_state (aiogram.dispatcher.filters.state.State): next state to set
        message_on_success (str): message to send to user if validation succeed
    """
    phone_number = re.sub(r"\s+", "", message.text)

    if not await phone_number_validator.validate(phone_number):
        return await message.answer(phone_number_validator.valid_format)

    async with state.proxy() as data:
        data["phone_number"] = phone_number

    await message.answer(message_on_success)

    await state.set_state(next_state)


async def full_name_handler(
        message: Message,
        state: FSMContext,
        next_state: str,
        message_on_success: str
):
    """
    Message handler for full name

    Args:
        message (aiogram.types.Message): message from user
        state (aiogram.dispatcher.FSMContext): current state
        next_state (aiogram.dispatcher.filters.state.State): next state to set
        message_on_success (str): message to send to user if validation succeed
    """
    full_name = re.sub(r"\s+", " ", message.text).strip().title()

    if not await full_name_validator.validate(full_name):
        return await message.answer(full_name_validator.valid_format)

    async with state.proxy() as data:
        data["full_name"] = full_name

        await message.answer(message_on_success)
        await state.set_state(next_state)


@get_strings_decorator(module="buttons")
async def text_handler(
        strings: Strings,
        message: Message,
        validator: AbstractValidator,
        state: FSMContext,
        next_state: str,
        message_on_success: str
):
    """
    Message handler for text

    Args:
        strings (tgbot.utils.language.Strings)
        message (aiogram.types.Message): message from user
        validator (tgbot.utils.validators.AbstractValidator): validator for data validation
        state (aiogram.dispatcher.FSMContext): current state
        next_state (aiogram.dispatcher.filters.state.State): next state to set
        message_on_success (str): message to send to user if validation succeed
    """
    tz = pytz.timezone(config.tg_bot.timezone)

    text = re.sub(r"\s+", " ", message.text).strip()
    date = message.date.astimezone(tz).strftime("%d.%m.%Y : %H:%M")

    if not await validator.validate(text):
        return await message.answer(validator.valid_format)

    async with state.proxy() as data:
        data["date"] = date
        data["text"] = text

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=strings["skip_image"], callback_data="skip")
            ]
        ]
    )
    await message.answer(message_on_success, reply_markup=kb)
    await state.set_state(next_state)


@get_strings_decorator(module="buttons")
async def skip_image_handler(
        strings: Strings,
        call: CallbackQuery,
        user: UserModel,
        state: FSMContext,
        message_on_success: str,
        message_on_fail: str,
):
    """
    Callback Query handler for skip image step

    Args:
        user (tgbot.services.database.UserModel):
        strings (tgbot.utils.language.Strings):
        call (aiogram.types.CallbackQuery): callback query from user
        state (aiogram.dispatcher.FSMContext): current state
        message_on_success (str): message to send to user if everything succeed
        message_on_fail (str): message to send to user if error have happened
    """
    await call.answer()

    next_state = Menus.notVerifiedUserMenu if user is None else Menus.verifiedUserMenu
    kb = not_verified_user_kb if user is None else verified_user_kb

    try:
        async with state.proxy() as data:
            caption = await format_message_to_support(
                additional_info=data.get("additional_info"),
                flat_number=data.get("flat_number"),
                phone_number=data.get("phone_number"),
                full_name=data.get("full_name"),
                date=data.get("date"),
                text=data.get("text")
            )

        await call.message.bot.send_message(chat_id=config.channels.support, text=caption)
    except (AttributeError, ChatNotFound):
        log.exception("Error while sending message to support channel")
        await call.message.answer(message_on_fail)
    else:
        await call.message.answer(message_on_success)

    await call.message.answer(
        mrd.bold(strings["main_menu"]),
        reply_markup=kb
    )

    await state.finish()
    await state.set_state(next_state)


@get_strings_decorator(module="buttons")
async def image_handler(
        strings: Strings,
        message: Message,
        user: UserModel,
        state: FSMContext,
        message_on_success: str,
        message_on_fail: str,
        album: List[Message],
):
    """
    Message handler for images

    Args:
        user (tgbot.services.database.UserModel):
        strings (tgbot.utils.language.Strings):
        message (aiogram.types.Message): message from user
        state (aiogram.dispatcher.FSMContext): current state
        message_on_success (str): message to send to user if everything succeed
        message_on_fail (str): message to send to user if error have happened
        album (List[aiogram.types.Message]): list of messages from which extract photos or documents
    """
    media_group = MediaGroup()

    next_state = Menus.notVerifiedUserMenu if user is None else Menus.verifiedUserMenu
    kb = not_verified_user_kb if user is None else verified_user_kb

    for obj in album:
        if obj.photo:
            file_id = obj.photo[-1].file_id
        else:
            file_id = obj[obj.content_type].file_id

        try:
            media_group.attach({"media": file_id, "type": obj.content_type})
        except ValueError:
            return await message.answer(
                strings.get_strings(mas_name_="STRINGS", module_="warnings")["document_type_not_supported"]
            )

    try:
        async with state.proxy() as data:
            caption = await format_message_to_support(
                additional_info=data.get("additional_info"),
                flat_number=data.get("flat_number"),
                phone_number=data.get("phone_number"),
                full_name=data.get("full_name"),
                date=data.get("date"),
                text=data.get("text")
            )

        media_group.media[0].caption = caption
        await message.bot.send_media_group(chat_id=config.channels.support, media=media_group)
    except (AttributeError, ChatNotFound):
        log.exception("Error while sending message to support channel")
        await message.answer(message_on_fail)
    else:
        await message.answer(message_on_success)

    await message.answer(
        mrd.bold(strings["main_menu"]),
        reply_markup=kb
    )

    await state.finish()
    await state.set_state(next_state)
