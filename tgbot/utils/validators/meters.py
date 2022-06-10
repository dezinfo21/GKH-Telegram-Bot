""" Meters validator """
from dataclasses import dataclass

from .abs_validator import AbstractValidator
from ..language import get_strings_sync


@dataclass
class FlatNumberValidator(AbstractValidator):
    """ Validator for meters """

    async def validate(self, meters_str: str) -> bool:
        meters = meters_str.replace(" ", "")

        return meters.isnumeric()


strings = get_strings_sync(module="valid_formats")

meters_validator = FlatNumberValidator(
    format_=strings["meters"]
)
