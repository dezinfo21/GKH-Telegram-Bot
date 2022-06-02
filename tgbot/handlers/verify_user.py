""" User verification module """
import re
from typing import NoReturn

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message

from tgbot.keyboards.default import main_kb, not_verified_user_kb, verified_user_kb
from tgbot.states import UserVerification, Menus
from tgbot.handlers import handlers
from tgbot.services import database
from tgbot.utils.language import get_strings_decorator, Strings, get_strings_sync
from tgbot.utils.validators import account_number_validator, \
    full_name_validator


@get_strings_decorator(module="contact_info")
async def verify_user(message: Message, strings: Strings, state: FSMContext):
    """
    Message handler to verify new user

    Args:
        message (aiogram.types.Message):
        strings (tgbot.utils.language.Strings):
        state (aiogram.dispatcher.FSMContext):
    """
    await message.answer(strings.get_strings(mas_name_="STRINGS", module_="buttons")["main_menu"])
    await message.answer(strings["flat_number"], reply_markup=main_kb)

    await state.set_state(UserVerification.flatNumber)


@get_strings_decorator(module="contact_info")
async def user_flat_number(message: Message, strings: Strings, state: FSMContext):
    """
    Message handler to get user's flat number

    Args:
        message (aiogram.types.Message):
        strings (tgbot.utils.language.Strings):
        state (aiogram.dispatcher.FSMContext):
    """
    await handlers.flat_number_handler(
        message=message,
        state=state,
        next_state=UserVerification.phoneNumber,
        message_on_success=strings["phone_number"]
    )


@get_strings_decorator(module="contact_info")
async def user_phone_number(message: Message, strings: Strings, state: FSMContext):
    """
    Message handler to get user's phone number

    Args:
        message (aiogram.types.Message):
        strings (tgbot.utils.language.Strings):
        state (aiogram.dispatcher.FSMContext):
    """
    await handlers.phone_number_handler(
        message=message,
        state=state,
        next_state=UserVerification.accountNumber,
        message_on_success=strings["account_number"]
    )


@get_strings_decorator(module="contact_info")
async def user_account_number(message: Message, strings: Strings, state: FSMContext):
    """
    Message handler to get user's account number

    Args:
        message (aiogram.types.Message):
        strings (tgbot.utils.language.Strings):
        state (aiogram.dispatcher.FSMContext):
    """
    account_number = message.text[-5:]

    if not await account_number_validator.validate(account_number):
        return await message.answer(account_number_validator.valid_format)

    async with state.proxy() as data:
        data["account_number"] = account_number

    await message.answer(strings["full_name"])
    await state.set_state(UserVerification.fullName)


@get_strings_decorator(module="contact_info")
async def user_full_name(message: Message, strings: Strings, state: FSMContext):
    """
    Message handler to get user's full name

    Args:
        message (aiogram.types.Message):
        strings (tgbot.utils.language.Strings):
        state (aiogram.dispatcher.FSMContext):
    """
    user_id = message.from_user.id
    full_name = re.sub(r"\s+", " ", message.text).strip().title()

    if not await full_name_validator.validate(full_name):
        return await message.answer(full_name_validator.valid_format)

    async with state.proxy() as data:
        data["full_name"] = full_name

    ver_notes: dict[str, str] = strings.get_strings(mas_name_="STRINGS", module_="verification")

    if database.save_user(
            user_id, data["flat_number"], data["phone_number"], data["account_number"], data["full_name"]
    ):
        await message.answer(
            ver_notes["success"].format(full_name=full_name), reply_markup=verified_user_kb
        )

        await state.finish()
        await state.set_state(Menus.verifiedUserMenu)

    else:
        await message.answer(
            ver_notes["fail"], reply_markup=not_verified_user_kb
        )

        await state.finish()
        await state.set_state(Menus.notVerifiedUserMenu)


def register_verification(dp: Dispatcher) -> NoReturn:
    """
    Register user verification handlers

    Args:
        dp (aiogram.Dispatcher):

    Returns:
        NoReturn
    """
    strings = get_strings_sync(module="buttons")

    dp.register_message_handler(
        verify_user,
        Text(equals=strings["verify_user"]),
        state=Menus.notVerifiedUserMenu
    )
    dp.register_message_handler(
        user_flat_number,
        state=UserVerification.flatNumber
    )
    dp.register_message_handler(
        user_phone_number,
        state=UserVerification.phoneNumber
    )
    dp.register_message_handler(
        user_account_number,
        state=UserVerification.accountNumber
    )
    dp.register_message_handler(
        user_full_name,
        state=UserVerification.fullName,
    )
