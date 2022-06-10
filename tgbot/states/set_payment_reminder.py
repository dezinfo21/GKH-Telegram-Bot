""" Set payment reminder states """
from aiogram.dispatcher.filters.state import StatesGroup, State


class SetPaymentReminder(StatesGroup):
    date = State()
    firstDate = State()
    secondDate = State()
