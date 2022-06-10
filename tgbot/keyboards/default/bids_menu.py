""" Bids keyboard """
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from tgbot.utils.language import get_strings_sync

strings = get_strings_sync(module="buttons")

bids_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(strings["new_bid"]),
            KeyboardButton(strings["req_inquiry"]),
        ],
        [
            KeyboardButton(strings["call_specialist"]),
        ],
        [
            KeyboardButton(strings["support"]),
        ],
        [
            KeyboardButton(strings["main_menu"])
        ]
    ],
    resize_keyboard=True
)
