""" Scheduler module """
import asyncio
import logging
from datetime import datetime
from typing import NoReturn

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from tgbot.data.config import load_config
from tgbot.services.database import get_users, get_user_debt
from tgbot.utils.language import get_strings_decorator, Strings

config = load_config(".env")
log = logging.getLogger(__name__)
bot = Bot(token=config.tg_bot.token, parse_mode='HTML')


async def notify_user(user_id: int, message: str) -> NoReturn:
    """
    Notify particular user with particular message

    Args:
        user_id (int):
        message (str):
    """
    try:
        await bot.send_message(chat_id=user_id, text=message)
    except Exception:
        log.exception(f"Пользователь с ID [{user_id}] заблокировал или удалил бота.")


@get_strings_decorator(module="notifications")
async def check_users_reminders(strings: Strings):
    """
    Checks each user's reminder and notifies them if it's the right time

    Args:
        strings (tgbot.utils.language.Strings):

    Returns:
        NoReturn
    """
    day = datetime.now().day

    users = await get_users()

    for user in users:
        if user.pay_rem_first_date == day or user.pay_rem_second_date == day:
            debt = await get_user_debt(user.account_number)

            await notify_user(
                user.user_id,
                strings["make_payment"].format(
                    account_number=user.account_number,
                    billing_period=debt.billing_period,
                    money_sum_with_debt=debt.money_sum_with_debt,
                )
            )

        if user.rem_send_meters:
            await notify_user(user.user_id, strings["send_meters"])

        await asyncio.sleep(.2)


def setup() -> NoReturn:
    """
    Configure scheduler

    Returns:
        NoReturn
    """
    log.info("Configure scheduler...")
    scheduler.add_job(
        check_users_reminders,
        trigger="cron",
        hour=config.misc.remind_time_hours,
        minute=config.misc.remind_time_minutes
    )

    scheduler.start()


scheduler = AsyncIOScheduler(timezone=config.tg_bot.timezone)
