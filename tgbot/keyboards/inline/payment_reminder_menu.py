""" Payment reminders keyboard """
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.utils.language import get_strings_sync

strings = get_strings_sync(module="buttons")

payment_reminders_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(strings["one_time_month"], callback_data="one_time_month")
        ],
        [
            InlineKeyboardButton(strings["two_times_month"], callback_data="two_times_month")
        ]
    ]
)
