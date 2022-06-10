""" Choose service module """
import re
from typing import Tuple, List, NoReturn

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery, ContentType

from tgbot.handlers import handlers
from tgbot.keyboards.inline.callback_data import services_cd
from tgbot.services.database import get_user_decorator, UserModel
from tgbot.states import Menus, ContactSpecialist
from tgbot.utils.language import get_strings_decorator, Strings
from tgbot.utils.validators import text_validator


async def extract_info(description: str) -> Tuple[str, str]:
    """
    Extract service name and price from service description

    Args:
        description (str): service description

    Returns:
        Tuple[str, str]: separated service name and price
    """
    price = re.search(r"- \d+ руб\.$", description).group(0).strip()
    name = description.replace(price, "").strip()

    return name, price


@get_user_decorator
@get_strings_decorator(module="contact_info")
async def choose_service(
        call: CallbackQuery, user: UserModel, strings: Strings, callback_data: dict, state: FSMContext
):
    """
    Callback query handler to choose service type

    Args:
        call (aiogram.types.CallbackQuery):
        user (tgbot.utils.database.UserModel):
        strings (tgbot.utils.language.Strings):
        callback_data (aiogram.types.CallbackQuery):
        state (aiogram.dispatcher.FSMContext):
    """
    await call.message.delete()
    await call.message.answer(strings["text_service"])

    service_number = callback_data["id_"]
    service_name, service_price = await extract_info(
        call.message.reply_markup.inline_keyboard[int(service_number)][0].text
    )

    async with state.proxy() as data:
        data["additional_info"] = \
            strings.get_strings(
                mas_name_="STRINGS", module_="specialist_title"
            )[data["spec"]].format(service=service_name, price=service_price)
        data["flat_number"] = user.flat_number
        data["phone_number"] = user.phone_number
        data["full_name"] = user.full_name

    await state.set_state(ContactSpecialist.text)


@get_strings_decorator(module="contact_info")
async def service_text(message: Message, strings: Strings, state: FSMContext):
    """
    Message handler for service's text

    Args:
        message (aiogram.types.Message):
        strings (tgbot.utils.language.Strings):
        state (aiogram.dispatcher.FSMContext):
    """
    await handlers.text_handler(
        message=message,
        validator=text_validator,
        state=state,
        next_state=ContactSpecialist.image,
        message_on_success=strings["img_new_bid"]
    )


@get_user_decorator
@get_strings_decorator(module="contact_specialist")
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
@get_strings_decorator(module="contact_specialist")
async def service_image(message: Message, user: UserModel, strings: Strings, state: FSMContext):
    """
    Message handler for service's photo or document

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
@get_strings_decorator(module="contact_specialist")
async def service_album(
        message: Message, user: UserModel, strings: Strings, album: List[Message], state: FSMContext
):
    """
    Message handler for service's album of photos or documents
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


def register_choose_service(dp: Dispatcher) -> NoReturn:
    """
    Register handlers for choosing service type

    Args:
        dp (aiogram.Dispatcher):

    Returns:
        NoReturn
    """
    dp.register_callback_query_handler(
        choose_service,
        services_cd.filter(),
        state=Menus.servicesMenu
    )

    dp.register_message_handler(
        service_text,
        state=ContactSpecialist.text
    )

    dp.register_callback_query_handler(
        skip_image,
        Text(equals="skip"),
        state=ContactSpecialist.image,
    )

    dp.register_message_handler(
        service_image,
        is_media_group=False,
        content_types=[ContentType.PHOTO, ContentType.DOCUMENT],
        state=ContactSpecialist.image
    )

    dp.register_message_handler(
        service_album,
        is_media_group=True,
        content_types=[ContentType.PHOTO, ContentType.DOCUMENT],
        state=ContactSpecialist.image
    )
