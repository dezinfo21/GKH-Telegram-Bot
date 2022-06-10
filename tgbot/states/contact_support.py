""" Contact support states """
from aiogram.dispatcher.filters.state import StatesGroup, State


class ContactSupport(StatesGroup):
    flatNumber = State()
    phoneNumber = State()
    fullName = State()
    text = State()
    image = State()
