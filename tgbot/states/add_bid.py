""" Add bid states """
from aiogram.dispatcher.filters.state import StatesGroup, State


class AddBid(StatesGroup):
    text = State()
    image = State()
