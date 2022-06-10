""" Verified user keyboard """
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from tgbot.utils.language import get_strings_sync

strings = get_strings_sync(module="buttons")

verified_user_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(strings["add_bid"])
        ],
        [
            KeyboardButton(strings["emergency"])
        ],
        [
            KeyboardButton(strings["get_debt"]),
            KeyboardButton(strings["submit_meters"])
        ],
        [
            KeyboardButton(strings["news"]),
            KeyboardButton(strings["contacts"]),
            KeyboardButton(strings["about"])
        ]
    ],
    resize_keyboard=True
)
