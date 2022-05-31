""" Bids keyboard """
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from tgbot.utils.language import get_strings_decorator, Strings


@get_strings_decorator(module="bids_menu")
async def get_bids_kb(strings: Strings) -> ReplyKeyboardMarkup:
    bids_kb = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(strings["new_bid"]),
                KeyboardButton(strings["req_inquiry"]),
            ],
            [
                KeyboardButton(strings["call_spec"]),
            ],
            [
                KeyboardButton(strings["support"]),
            ],
            [
                KeyboardButton(strings["main_menu"])
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    return bids_kb
