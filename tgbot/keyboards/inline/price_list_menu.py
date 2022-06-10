""" Price list keyboard """
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from .callback_data import services_cd
from tgbot.services.database import get_specialist_price_list


async def format_service_info(service_name: str, service_price: int) -> str:
    """
    Format text for service button

    Args:
        service_name (str):
        service_price (int):

    Returns:
        str: formatted text for button
    """
    return f"{service_name} - {service_price} руб."


async def get_price_list_kb(specialist_id: str) -> InlineKeyboardMarkup | None:
    """
    Return price list keyboard for specialist with particular id

    Args:
        specialist_id (str):

    Returns:
        InlineKeyboardMarkup | None: inline keyboard if price list is not empty, otherwise None
    """
    price_list = await get_specialist_price_list(specialist_id)

    if price_list is None:
        return None

    kb = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(
            await format_service_info(service.name, service.price),
            callback_data=services_cd.new(id_=i)
        ) for i, service in enumerate(price_list)
    ]

    kb.add(*buttons)

    return kb
