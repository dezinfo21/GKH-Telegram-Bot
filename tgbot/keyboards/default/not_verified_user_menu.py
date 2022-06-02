""" Not verified user keyboard """
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from tgbot.utils.language import get_strings_sync

strings = get_strings_sync(module="buttons")

not_verified_user_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(strings["verify_user"])
        ],
        [
            KeyboardButton(strings["submit_meters"])
        ],
        [
            KeyboardButton(strings["contacts"]),
            KeyboardButton(strings["about"])
        ]
    ],
    resize_keyboard=True
)
