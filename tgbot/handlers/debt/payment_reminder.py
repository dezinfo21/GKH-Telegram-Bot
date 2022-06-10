""" Payment reminders module """
from typing import NoReturn

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import html_decoration as mrd

from tgbot.keyboards.default import debt_kb, back_kb
from tgbot.keyboards.inline import payment_reminders_kb, get_days_kb
from tgbot.keyboards.inline.callback_data import days_cd
from tgbot.services import database
from tgbot.states import Menus, SetPaymentReminder
from tgbot.utils.language import get_strings_decorator, Strings, get_strings_sync


@get_strings_decorator(module="buttons")
async def remind_payment(message: Message, strings: Strings, state: FSMContext):
    """
    Message handler for remind payment

    Args:
        message (aiogram.types.Message):
        strings (tgbot.utils.language.Strings):
        state (aiogram.dispatcher.FSMContext):
    """
    await message.answer(
        mrd.bold(strings["remind_payment"]),
        reply_markup=back_kb
    )
    await message.answer(
        strings.get_strings(mas_name_="STRINGS", module_="contact_info")["choose_payment_reminder"],
        reply_markup=payment_reminders_kb
    )

    await state.finish()
    await state.set_state(Menus.paymentRemindersMenu)


@get_strings_decorator(module="contact_info")
async def one_time_month_reminder(call: CallbackQuery, strings: Strings, state: FSMContext):
    """
    Callback query handler for one time month reminder

    Args:
        call (aiogram.types.CallbackQuery):
        strings (tgbot.utils.language.Strings):
        state (aiogram.dispatcher.FSMContext):
    """
    await call.answer()

    kb = await get_days_kb()
    await call.message.edit_text(
        strings["choose_reminder_date"],
        reply_markup=kb
    )

    await state.set_state(SetPaymentReminder.date)


@get_strings_decorator(module="contact_info")
async def two_times_month_reminder(call: CallbackQuery, strings: Strings, state: FSMContext):
    """
    Callback query handler for two times month reminder

    Args:
        call (aiogram.types.CallbackQuery):
        strings (tgbot.utils.language.Strings):
        state (aiogram.dispatcher.FSMContext):
    """
    await call.answer()

    kb = await get_days_kb()
    await call.message.edit_text(
        strings["choose_first_reminder_date"],
        reply_markup=kb
    )

    await state.set_state(SetPaymentReminder.firstDate)


@get_strings_decorator(module="set_payment_reminder_dates")
async def set_payment_reminder_date(
        call: CallbackQuery, strings: Strings, callback_data: dict, state: FSMContext
):
    """
    Callback query to set date for one time month reminder

    Args:
        call (aiogram.types.CallbackQuery):
        strings (tgbot.utils.language.Strings):
        callback_data (dict):
        state (aiogram.dispatcher.FSMContext):
    """
    await call.message.delete_reply_markup()

    date = callback_data["number"]

    if await database.set_user_payment_reminder_dates(user_id=call.from_user.id, first_date=date):
        await call.answer(strings["success"])
        await call.message.answer(strings["success"], reply_markup=debt_kb)
    else:
        await call.answer(strings["fail"])
        await call.message.answer(strings["fail"], reply_markup=debt_kb)

    await state.set_state(Menus.debtMenu)


@get_strings_decorator(module="contact_info")
async def set_first_payment_reminder_date(
        call: CallbackQuery, strings: Strings, callback_data: dict, state: FSMContext
):
    """
    Callback query to set first date for two times month reminder

    Args:
        call (aiogram.types.CallbackQuery):
        strings (tgbot.utils.language.Strings):
        callback_data (dict):
        state (aiogram.dispatcher.FSMContext):
    """
    await call.answer("Ok")
    await call.message.delete()

    first_date = callback_data["number"]

    async with state.proxy() as data:
        data["first_date"] = first_date

    kb = await get_days_kb()
    await call.message.answer(
        strings["choose_second_reminder_date"],
        reply_markup=kb
    )

    await state.set_state(SetPaymentReminder.secondDate)


@get_strings_decorator(module="set_payment_reminder_dates")
async def set_second_payment_reminder_date(
        call: CallbackQuery, strings: Strings, callback_data: dict, state: FSMContext
):
    """
    Callback query to set first date for two times month reminder

    Args:
        call (aiogram.types.CallbackQuery):
        strings (tgbot.utils.language.Strings):
        callback_data (dict):
        state (aiogram.dispatcher.FSMContext):
    """
    await call.message.delete()

    second_date = callback_data["number"]

    async with state.proxy() as data:
        first_date = data["first_date"]

    if await database.set_user_payment_reminder_dates(
            user_id=call.from_user.id, first_date=first_date, second_date=second_date
    ):
        await call.answer(strings["success"])
        await call.message.answer(strings["success"], reply_markup=debt_kb)
    else:
        await call.answer(strings["fail"])
        await call.message.answer(strings["fail"], reply_markup=debt_kb)

    await state.finish()
    await state.set_state(Menus.debtMenu)


def register_remind_payment(dp: Dispatcher) -> NoReturn:
    """
    Register payment reminders

    Args:
        dp (aiogram.Dispatcher):

    Returns:
        NoReturn
    """
    strings = get_strings_sync(module="buttons")

    dp.register_message_handler(
        remind_payment,
        Text(equals=[strings["remind_payment"], strings["back"]]),
        state=Menus.debtMenu
    )

    dp.register_callback_query_handler(
        one_time_month_reminder,
        Text(equals="one_time_month"),
        state=Menus.paymentRemindersMenu
    )

    dp.register_callback_query_handler(
        two_times_month_reminder,
        Text(equals="two_times_month"),
        state=Menus.paymentRemindersMenu
    )

    dp.register_callback_query_handler(
        set_payment_reminder_date,
        days_cd.filter(),
        state=SetPaymentReminder.date
    )

    dp.register_callback_query_handler(
        set_first_payment_reminder_date,
        days_cd.filter(),
        state=SetPaymentReminder.firstDate
    )

    dp.register_callback_query_handler(
        set_second_payment_reminder_date,
        days_cd.filter(),
        state=SetPaymentReminder.secondDate
    )
