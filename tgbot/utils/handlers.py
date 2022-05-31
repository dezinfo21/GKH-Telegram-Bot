import logging
import re
from typing import NoReturn, List

import pytz
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, MediaGroup, \
    ReplyKeyboardMarkup

from tgbot.data.config import load_config
from tgbot.utils import database
from tgbot.utils.validators import flat_number_validator, phone_number_validator, full_name_validator, text_validator

log = logging.getLogger(__name__)
config = load_config(".env")


async def beautify_info(flat_number: int, phone_number: int, full_name: str, date: str, text: str) -> str:
    contact_info = database.ContactInfo(flat_number, phone_number, full_name, date, text)

    caption = f"<b>ФИО</b>: {contact_info.full_name}\n" \
              f"<b>Контактный номер телефона</b>: +{contact_info.phone_number}\n" \
              f"<b>Квартира</b>: {contact_info.flat_number}\n" \
              f"<b>Дата</b>: {contact_info.date}\n\n" \
              f"{contact_info.text}"

    return caption


async def flat_number_handler(
        message: Message,
        state: FSMContext,
        state_on_success: str,
        message_on_success: str
) -> NoReturn:
    flat_number_str = message.text

    if await flat_number_validator.validate(flat_number_str):
        async with state.proxy() as data:
            data["flat_number"] = int(flat_number_str)

        await message.answer(message_on_success)
        await state.set_state(state_on_success)
    else:
        await message.answer(flat_number_validator.valid_format)


async def phone_number_handler(
        message: Message,
        state: FSMContext,
        state_on_success: str,
        message_on_success: str
) -> NoReturn:
    phone_number = re.sub(r"\s+", "", message.text)

    if await phone_number_validator.validate(phone_number):
        async with state.proxy() as data:
            data["phone_number"] = phone_number

        await message.answer(message_on_success)
        await state.set_state(state_on_success)
    else:
        await message.answer(phone_number_validator.valid_format)


async def full_name_handler(
        message: Message,
        state: FSMContext,
        state_on_success: str,
        message_on_success: str
) -> NoReturn:
    full_name = re.sub(r"\s+", " ", message.text).strip().title()

    if await full_name_validator.validate(full_name):
        async with state.proxy() as data:
            data["full_name"] = full_name

            await message.answer(message_on_success)
            await state.set_state(state_on_success)

    else:
        await message.answer(full_name_validator.valid_format)


async def text_handler(
        message: Message,
        state: FSMContext,
        state_on_success: str,
        message_on_success: str
) -> NoReturn:
    tz = pytz.timezone("Europe/Moscow")

    text = re.sub(r"\s+", " ", message.text).strip()
    date = message.date.astimezone(tz).strftime("%d.%m.%Y : %H:%M")

    if await text_validator.validate(text):
        async with state.proxy() as data:
            data["date"] = date
            data["text"] = text

        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="Отправить без фото", callback_data="skip")
                ]
            ]
        )
        await message.answer(message_on_success, reply_markup=kb)
        await state.set_state(state_on_success)

    else:
        await message.answer(text_validator.valid_format)


async def skip_image_handler(
        call: CallbackQuery,
        state: FSMContext,
        state_on_success: str,
        message_on_success: str,
        keyboard: ReplyKeyboardMarkup | None = None
) -> NoReturn:
    await call.answer()

    async with state.proxy() as data:
        caption = await beautify_info(*data.values())

    await call.message.bot.send_message(chat_id=config.channels.support, text=caption)

    await call.message.answer(
        message_on_success,
        reply_markup=keyboard
    )

    await state.set_state(state_on_success)


async def image_handler(
        message: Message,
        state: FSMContext,
        state_on_success: str,
        message_on_success: str,
        keyboard: ReplyKeyboardMarkup | None = None
) -> NoReturn:
    media_group = MediaGroup()

    if message.photo:
        file_id = message.photo[-1].file_id
    else:
        file_id = message[message.content_type].file_id

    try:
        media_group.attach({"media": file_id, "type": message.content_type})
    except ValueError:
        return await message.answer("!!Извините, данный тип документов не поддержуеться.")

    async with state.proxy() as data:
        caption = await beautify_info(*data.values())

    media_group.media[0].caption = caption
    await message.bot.send_media_group(chat_id=config.channels.support, media=media_group)

    await message.answer(
        message_on_success,
        reply_markup=keyboard
    )

    await state.set_state(state_on_success)


async def album_handler(
        message: Message,
        album: List[Message],
        state: FSMContext,
        state_on_success: str,
        message_on_success: str,
        keyboard: ReplyKeyboardMarkup | None = None
) -> NoReturn:
    media_group = MediaGroup()

    for obj in album:
        if obj.photo:
            file_id = obj.photo[-1].file_id
        else:
            file_id = obj[obj.content_type].file_id

        try:
            media_group.attach({"media": file_id, "type": obj.content_type})
        except ValueError:
            return await message.answer("!!Извините, данный тип документов не поддержуеться.")

    async with state.proxy() as data:
        caption = await beautify_info(*data.values())

    media_group.media[0].caption = caption
    await message.bot.send_media_group(chat_id=config.channels.support, media=media_group)

    await message.answer(
        message_on_success,
        reply_markup=keyboard
    )

    await state.set_state(state_on_success)
