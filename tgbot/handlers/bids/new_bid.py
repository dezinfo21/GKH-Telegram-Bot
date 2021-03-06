""" Bot new bid creation module """
from typing import List, NoReturn

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery, ContentType

from tgbot.data.config import load_config
from tgbot.handlers import handlers
from tgbot.keyboards.default import back_kb
from tgbot.services.database import get_user_decorator, UserModel
from tgbot.states import Menus, AddBid
from tgbot.utils.language import get_strings_sync, get_strings_decorator, Strings
from tgbot.utils.validators import text_validator

config = load_config(".env")


@get_user_decorator
@get_strings_decorator(module="contact_info")
async def new_bid(message: Message, user: UserModel, strings: Strings, state: FSMContext):
    """
    Message handler for new bid

    Args:
        message (aiogram.types.Message):
        user (tgbot.services.database.UserModel):
        strings (tgbot.utils.language.Strings):
        state (aiogram.dispatcher.FSMContext):
    """
    await message.answer(
        strings.get_strings(mas_name_="STRINGS", module_="buttons")["new_bid"],
        reply_markup=back_kb
    )
    await message.answer(strings["text_new_bid"])

    async with state.proxy() as data:
        data["flat_number"] = user.flat_number
        data["phone_number"] = user.phone_number
        data["full_name"] = user.full_name

    await state.set_state(AddBid.text)


@get_strings_decorator(module="contact_info")
async def bid_text(message: Message, strings: Strings, state: FSMContext):
    """
    Message handler for bid's text

    Args:
        message (aiogram.types.Message):
        strings (tgbot.utils.language.Strings):
        state (aiogram.dispatcher.FSMContext):
    """
    await handlers.text_handler(
        message=message,
        validator=text_validator,
        state=state,
        next_state=AddBid.image,
        message_on_success=strings["img_new_bid"]
    )


@get_user_decorator
@get_strings_decorator(module="new_bid")
async def skip_image(call: CallbackQuery, user: UserModel, strings: Strings, state: FSMContext):
    """
    Callback query handler to skip image step

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
        message_on_fail=strings["fail"],
    )


@get_user_decorator
@get_strings_decorator(module="new_bid")
async def bid_image(message: Message, user: UserModel, strings: Strings, state: FSMContext):
    """
    Message handler for bid's photo or document

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
        album=[message],
    )


@get_user_decorator
@get_strings_decorator(module="new_bid")
async def bid_album(
        message: Message, user: UserModel, strings: Strings, album: List[Message], state: FSMContext
):
    """
    Message handler for bid's album of photos or documents
    Args:
        message (aiogram.types.Message):
        user (tgbot.services.database.UserModel):
        strings (tgbot.utils.language.Strings):
        album (List[aiogram.types.Message])
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


def register_new_bid(dp: Dispatcher) -> NoReturn:
    """
    Register handlers for new bid creation

    Args:
        dp (aiogram.Dispatcher):

    Returns:
        NoReturn
    """
    strings = get_strings_sync(module="buttons")

    dp.register_message_handler(
        new_bid,
        Text(equals=strings["new_bid"]),
        verified_only=True,
        state=Menus.bidsMenu
    )

    dp.register_message_handler(
        bid_text,
        state=AddBid.text
    )

    dp.register_callback_query_handler(
        skip_image,
        Text(equals="skip"),
        state=AddBid.image,
    )

    dp.register_message_handler(
        bid_image,
        is_media_group=False,
        content_types=[ContentType.PHOTO, ContentType.DOCUMENT],
        state=AddBid.image
    )

    dp.register_message_handler(
        bid_album,
        is_media_group=True,
        content_types=[ContentType.PHOTO, ContentType.DOCUMENT],
        state=AddBid.image
    )
