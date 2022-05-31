""" Not verified user keyboard """
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from tgbot.utils.language import get_strings_decorator, Strings


@get_strings_decorator(module="user_menu")
async def get_not_ver_user_kb(strings: Strings) -> ReplyKeyboardMarkup:
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

    return not_verified_user_kb
