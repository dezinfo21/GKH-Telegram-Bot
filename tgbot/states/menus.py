""" Menus """
from aiogram.dispatcher.filters.state import StatesGroup, State


class Menus(StatesGroup):
    notVerifiedUserMenu = State()
    verifiedUserMenu = State()
    contactsMenu = State()
    emergencyContactsMenu = State()
    debtMenu = State()
    paymentRemindersMenu = State()
    bidsMenu = State()
    specialistsMenu = State()
    servicesMenu = State()
    metersMenu = State()
