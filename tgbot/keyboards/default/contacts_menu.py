""" Contacts keyboard """
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from tgbot.utils.language import get_strings_sync

strings = get_strings_sync(module="buttons")

contacts_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=strings["emerg_contacts"])
        ],
        [
            KeyboardButton(text=strings["support"])
        ],
        [
            KeyboardButton(text=strings["main_menu"])
        ]
    ],
    resize_keyboard=True
)
