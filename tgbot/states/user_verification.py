""" User verification states """
from aiogram.dispatcher.filters.state import StatesGroup, State


class UserVerification(StatesGroup):
    flatNumber = State()
    phoneNumber = State()
    accountNumber = State()
    fullName = State()
