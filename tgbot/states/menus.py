from aiogram.dispatcher.filters.state import StatesGroup, State


class Menus(StatesGroup):
    notVerifiedUserMenu = State()
    verifiedUserMenu = State()
    contactsMenu = State()
    emergencyContactsMenu = State()
    bidsMenu = State()
