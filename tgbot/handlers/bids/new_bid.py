import re
from typing import List

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, MediaGroup, ContentType

from tgbot.data.config import load_config
from tgbot.keyboards.default import bids_kb, main_kb
from tgbot.states import Menus, Bid
from tgbot.utils import database
from tgbot.utils.validators import text_validator

config = load_config(".env")


async def beautify_bid_info(flat_number: int, phone_number: int, full_name: str, date: str, text: str) -> str:
    bid_info = database.BidModel(flat_number, phone_number, full_name, date, text)

    caption = f"<b>ФИО</b>: {bid_info.full_name}\n"\
              f"<b>Контактный номер телефона</b>: +{bid_info.phone_number}\n" \
              f"<b>Квартира</b>: {bid_info.flat_number}\n" \
              f"<b>Дата</b>: {bid_info.date}\n\n" \
              f"{bid_info.text}"

    return caption


async def new_bid(message: Message, state: FSMContext):
    await message.answer("<b>Новая заявка</b>", reply_markup=main_kb)

    await message.answer("<b>Введите текст вашей заяки</b>")
    await state.set_state(Bid.text)


async def bid_text(message: Message, user: database.UserModel, state: FSMContext):
    text = re.sub(r"\s+", " ", message.text).strip()
    date = message.date.strftime("%d.%m.%Y : %H:%M")

    if await text_validator.validate(text):
        async with state.proxy() as data:
            data["flat_number"] = user.flat_number
            data["phone_number"] = user.phone_number
            data["full_name"] = user.full_name
            data["date"] = date
            data["text"] = text

        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="Отправить без фото", callback_data="skip")
                ]
            ]
        )
        await message.answer("<b>Если требуеться, приложите фотографии к вашей заявке</b>", reply_markup=kb)
        await state.set_state(Bid.image)

    else:
        await message.answer(text_validator.valid_format)


async def skip_image(call: CallbackQuery, state: FSMContext):
    await call.answer()

    async with state.proxy() as data:
        caption = await beautify_bid_info(*data.values())

    await call.message.bot.send_message(chat_id=config.channels.support, text=caption)

    await call.message.answer(
        "Ваша заявка была успешно отправленна. Ожидайте скорого ответа.",
        reply_markup=bids_kb
    )

    await state.finish()
    await state.set_state(Menus.bidsMenu)


async def bid_image(message: Message, state: FSMContext):
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
        caption = await beautify_bid_info(*data.values())

    media_group.media[0].caption = caption
    await message.bot.send_media_group(chat_id=config.channels.support, media=media_group)

    await message.answer(
        "Ваша заявка была успешно отправленна. Ожидайте скорого ответа.",
        reply_markup=bids_kb
    )

    await state.finish()
    await state.set_state(Menus.bidsMenu)


async def bid_album(message: Message, user: database.UserModel, album: List[Message], state: FSMContext):
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
        caption = await beautify_bid_info(*data.values())

    media_group.media[0].caption = caption
    await message.bot.send_media_group(chat_id=config.channels.support, media=media_group)

    await message.answer(
        "Ваша заявка была успешно отправленна. Ожидайте скорого ответа.",
        reply_markup=bids_kb
    )

    await state.finish()
    await state.set_state(Menus.bidsMenu)


def register_new_bid(dp: Dispatcher):
    dp.register_message_handler(
        new_bid,
        Text(equals="Новая заявка"),
        verified_only=True,
        state=Menus.bidsMenu
    )
    dp.register_message_handler(
        bid_text,
        state=Bid.text
    )
    dp.register_callback_query_handler(
        skip_image,
        Text(equals="skip"),
        state=Bid.image,
    )
    dp.register_message_handler(
        bid_image,
        is_media_group=False,
        content_types=[ContentType.PHOTO, ContentType.DOCUMENT],
        state=Bid.image
    )
    dp.register_message_handler(
        bid_album,
        is_media_group=True,
        content_types=[ContentType.PHOTO, ContentType.DOCUMENT],
        state=Bid.image
    )
