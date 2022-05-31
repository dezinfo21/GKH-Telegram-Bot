import re

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message

from tgbot.keyboards.default import get_main_kb, get_not_ver_user_kb, get_ver_user_kb
from tgbot.states import UserVerification, Menus
from tgbot.utils import database as db
from tgbot.utils.validators import flat_number_validator, phone_number_validator, account_number_validator, \
    full_name_validator
from tgbot.utils.language import get_strings_decorator


@get_strings_decorator(module="contact_info")
async def verify_user(message: Message, state: FSMContext):
    kb = await get_main_kb()
    await message.answer("<b>Верификация статуса жильца</b>", reply_markup=kb)

    await message.answer("<b>Введите ваш номер квартиры</b>")

    await state.set_state(UserVerification.flatNumber)


async def user_flat_number(message: Message, state: FSMContext):
    flat_number_str = message.text

    if not await flat_number_validator.validate(flat_number_str):
        return await message.answer(flat_number_validator.valid_format)

    async with state.proxy() as data:
        data["flat_number"] = int(flat_number_str)

    await message.answer("<b>Введите номер телефона по которому с вами можно связаться, в формате 7 999 999 99 99</b>")
    await state.set_state(UserVerification.phoneNumber)


async def user_phone_number(message: Message, state: FSMContext):
    phone_number = message.text

    if not await phone_number_validator.validate(phone_number):
        return await message.answer(phone_number_validator.valid_format)

    async with state.proxy() as data:
        data["phone_number"] = phone_number

    await message.answer("<b>Укажите ваш номер лицевого счета</b>")
    await state.set_state(UserVerification.accountNumber)


async def user_account_number(message: Message, state: FSMContext):
    account_number = message.text[-5:]

    if not await account_number_validator.validate(account_number):
        return await message.answer(account_number_validator.valid_format)

    async with state.proxy() as data:
        data["account_number"] = account_number

    await message.answer("<b>Укажите ваши ФИО</b>")
    await state.set_state(UserVerification.fullName)


async def user_full_name(message: Message, state: FSMContext):
    user_id = message.from_user.id
    full_name = re.sub(r"\s+", " ", message.text).strip().title()

    if not await full_name_validator.validate(full_name):
        return await message.answer(full_name_validator.valid_format)

    async with state.proxy() as data:
        data["full_name"] = full_name

    if db.save_user(
            user_id, data["flat_number"], data["phone_number"], data["account_number"], data["full_name"]
    ):
        kb = await get_ver_user_kb()
        await message.answer(
            f"Пользователь <b>{full_name}</b> успешно верефецирован.", reply_markup=kb
        )

        await state.finish()
        await state.set_state(Menus.verifiedUserMenu)

    else:
        kb = await get_not_ver_user_kb()
        await message.answer(
            "Упс... Что то пошло не так, попробуйте в другой раз.", reply_markup=kb
        )

        await state.finish()
        await state.set_state(Menus.notVerifiedUserMenu)


def register_verification(dp: Dispatcher):
    dp.register_message_handler(
        verify_user,
        Text(equals="Верификация статуса жильца"),
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
