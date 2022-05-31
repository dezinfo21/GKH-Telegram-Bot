""" Main menu keyboard """
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from tgbot.utils.language import get_strings_decorator, Strings


@get_strings_decorator(module="main_menu")
async def get_main_kb(strings: Strings) -> ReplyKeyboardMarkup:
    main_kb = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(strings["main"])
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    return main_kb
