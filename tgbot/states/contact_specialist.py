""" Contact specialist states """
from aiogram.dispatcher.filters.state import StatesGroup, State


class ContactSpecialist(StatesGroup):
    text = State()
    image = State()
