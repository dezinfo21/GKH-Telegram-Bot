""" Meters keyboard """
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from .callback_data import meters_cd
from tgbot.utils.language import get_strings_decorator, Strings


@get_strings_decorator(module="buttons")
async def get_meters_kb(strings: Strings, remind_send_meters: bool | None = None) -> InlineKeyboardMarkup:
    """
    Return keyboard with meters actions

    Args:
        strings (tgbot.utils.language.Strings):
        remind_send_meters (bool): whether remind user to send meters or not

    Returns:
         InlineKeyboardMarkup
    """
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(strings["electrician_meters"], callback_data=meters_cd.new(type_="electrician")),
            ],
            [
                InlineKeyboardButton(strings["water_meters"], callback_data=meters_cd.new(type_="water"))
            ]
        ]
    )

    if remind_send_meters is not None:
        text = strings["not_remind_send_meters"] if remind_send_meters else strings["remind_send_meters"]
        kb.row(InlineKeyboardButton(text, callback_data="remind_send_meters"))

    return kb
