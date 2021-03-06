""" Contacts keyboard """
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from tgbot.utils.language import get_strings_sync

strings = get_strings_sync(module="buttons")

contacts_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(strings["emergency_contacts"])
        ],
        [
            KeyboardButton(strings["support"])
        ],
        [
            KeyboardButton(strings["main_menu"])
        ]
    ],
    resize_keyboard=True
)
