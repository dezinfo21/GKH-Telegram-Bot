from aiogram.dispatcher.filters.state import StatesGroup, State


class ContactForm(StatesGroup):
    flatNumber = State()
    phoneNumber = State()
    fullName = State()
    text = State()
    image = State()
