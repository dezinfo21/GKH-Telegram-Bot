""" Contacts keyboard """
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from tgbot.utils.language import get_strings_decorator, Strings


@get_strings_decorator(module="main_menu")
async def get_contacts_kb(strings: Strings):
    contacts_kb = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Телефоны Экстренных служб")
            ],
            [
                KeyboardButton(text="Обращение к Руководителю")
            ],
            [
                KeyboardButton(text="Главное меню")
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    return contacts_kb
