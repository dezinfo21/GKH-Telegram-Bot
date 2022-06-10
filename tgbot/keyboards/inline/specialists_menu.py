""" Specialists keyboard """
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from .callback_data import specialists_cd
from tgbot.utils.language import get_strings_sync

strings = get_strings_sync(module="buttons")


specialists_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                strings["plumber"],
                callback_data=specialists_cd.new(spec="plumber")
            )
        ],
        [
            InlineKeyboardButton(
                strings["electrician"],
                callback_data=specialists_cd.new(spec="electrician")
            )
        ]
    ]
)
