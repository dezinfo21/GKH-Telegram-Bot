""" Callback data module """
from aiogram.utils.callback_data import CallbackData

specialists_cd = CallbackData("specialist", "spec")
services_cd = CallbackData("service", "id_")
days_cd = CallbackData("day", "number")
meters_cd = CallbackData("meters", "type_")
