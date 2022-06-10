""" Debt keyboard """
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from tgbot.utils.language import get_strings_sync

strings = get_strings_sync(module="buttons")


debt_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(strings["pay_debt"]),
            KeyboardButton(strings["remind_payment"])
        ],
        [
            KeyboardButton(strings["main_menu"])
        ]
    ],
    resize_keyboard=True
)

