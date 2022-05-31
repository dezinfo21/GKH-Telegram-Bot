""" Verified user keyboard """
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from tgbot.utils.language import get_strings_decorator, Strings


@get_strings_decorator(module="user_menu")
async def get_ver_user_kb(strings: Strings) -> ReplyKeyboardMarkup:
    verified_user_kb = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(strings["add_bid"])
            ],
            [
                KeyboardButton(strings["get_debt"])
            ],
            [
                KeyboardButton(strings["emergency"])
            ],
            [
                KeyboardButton(strings["submit_meters"])
            ],
            [
                KeyboardButton(strings["news"])
            ],
            [
                KeyboardButton(strings["contacts"]),
                KeyboardButton(strings["about"])
            ]
        ],
        resize_keyboard=True
    )

    return verified_user_kb
