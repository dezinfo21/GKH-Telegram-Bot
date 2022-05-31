from aiogram.dispatcher.filters.state import StatesGroup, State


class Bid(StatesGroup):
    text = State()
    image = State()
