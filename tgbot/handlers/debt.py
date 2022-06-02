""" Bot module to get user's debt """
from typing import NoReturn

from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import Message

from tgbot.services import database
from tgbot.services.database import get_user_decorator
from tgbot.states import Menus
from tgbot.utils.language import get_strings_sync, get_strings_decorator, Strings


@get_user_decorator
@get_strings_decorator(module="debt")
async def get_debt(message: Message, user: database.UserModel, strings: Strings):
    """
    Message handler to get user's debt

    Args:
        message (aiogram.types.Message):
        user (tgbot.services.database.UserModel):
        strings (tgbot.utils.language.Strings):
    """
    debt = await database.get_user_debt(user.account_number)

    caption = strings["main_text"].format(
        account_number=user.account_number,
        billing_period=debt.billing_period,
        money_sum_with_debt=debt.money_sum_with_debt,
        placement_date=debt.placement_date
    )

    if debt.money_paid == 0:
        caption += strings["miss_payment"]
    else:
        caption += strings["last_payment"].format(
            money_paid=debt.money_paid,
            last_payment_date=debt.last_payment_date
        )

    await message.answer(caption)


def register_debt(dp: Dispatcher) -> NoReturn:
    """
    Register get debt handler

    Args:
        dp (aiogram.Dispatcher):

    Returns:
        NoReturn
    """
    strings = get_strings_sync(module="buttons")

    dp.register_message_handler(
        get_debt,
        Text(equals=strings["get_debt"]),
        state=Menus.verifiedUserMenu
    )
