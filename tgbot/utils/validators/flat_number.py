""" Flat number validator """
from dataclasses import dataclass

from .abs_validator import AbstractValidator
from ..language import get_strings_sync


@dataclass
class FlatNumberValidator(AbstractValidator):
    """
    Validator for flat number

    Attributes:
        min_value (int): minimum value for flat number
        max_value (int): maximum value for flat number
    """
    min_value: int
    max_value: int

    async def validate(self, flat_number_str: str) -> bool:
        try:
            flat_number = int(flat_number_str)
        except ValueError:
            return False

        return self.min_value < flat_number < self.max_value


strings = get_strings_sync(module="valid_formats")

flat_number_validator = FlatNumberValidator(
    min_value=1,
    max_value=78,
    format_=strings["flat_number"]
)
