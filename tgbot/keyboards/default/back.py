""" Back keyboard """
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from tgbot.utils.language import get_strings_sync

strings = get_strings_sync(module="buttons")

back_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(strings.get_strings(mas_name_="STRINGS", module_="buttons")["back"])
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
