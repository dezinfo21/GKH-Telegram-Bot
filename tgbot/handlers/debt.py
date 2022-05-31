from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import Message

from tgbot.states import Menus
from tgbot.utils import database


async def user_debt(message: Message, user: database.UserModel):
    debt = database.get_user_debt(user.account_number)

    caption = (
        f"По лицевому счету <b>{user.account_number}</b> за расчётный период "
        f"<b>{debt.billing_period}</b> начислено к оплате <b>{debt.money_sum_with_debt}</b> "
        f"руб. Оплату произвести до {debt.placement_date}\n\n"
    )

    if debt.money_paid == 0:
        caption += (
            "!! Пропущен ежемесячный платёж по оплате. Субсидии и иные меры соц.поддержки граждан "
            "могут быть скорректированы или отменены и начислены пени."
        )
    else:
        caption += (
            f"Последний поступивший учтеный платёж <b>{debt.money_paid}</b> руб. от "
            f"<b>{debt.last_payment_date}</b>"
        )

    await message.answer(caption)


def register_debt(dp: Dispatcher):
    dp.register_message_handler(
        user_debt,
        Text(equals="Узнать задолженность"),
        state=Menus.verifiedUserMenu
    )
