""" Main menu keyboard """
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from tgbot.utils.language import get_strings_sync

strings = get_strings_sync(module="buttons")

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(strings["main_menu"])
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
