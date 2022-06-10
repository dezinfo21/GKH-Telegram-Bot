""" Days keyboard """
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from .callback_data import days_cd


async def get_days_kb() -> InlineKeyboardMarkup:
    """
    Create and return keyboard of days

    Returns:
        aiogram.types.InlineKeyboardMarkup
    """
    kb = InlineKeyboardMarkup(row_width=4)
    buttons = [
        InlineKeyboardButton(
            str(day),
            callback_data=days_cd.new(number=day)
        ) for day in range(1, 25)
    ]

    kb.add(*buttons)

    return kb
