""" Send meters states """
from aiogram.dispatcher.filters.state import StatesGroup, State


class SendMeters(StatesGroup):
    flatNumber = State()
    text = State()
    image = State()
