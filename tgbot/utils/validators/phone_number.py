""" Phone number validator """
import re
from dataclasses import dataclass, InitVar

from .abs_validator import AbstractValidator
from ..language import get_strings_sync


@dataclass
class PhoneNumberValidator(AbstractValidator):
    """
    Validator for phone number

    Attributes:
        regex (InitVar[str]): regular expression for pattern,
        which will be used to validate phone number
    """
    regex: InitVar[str]

    def __post_init__(self, format_: str, regex: str):
        self._format = format_
        self.pattern = re.compile(regex)

    async def validate(self, phone_number: str) -> bool:
        return bool(self.pattern.match(phone_number))


strings = get_strings_sync(module="valid_formats")

phone_number_validator = PhoneNumberValidator(
    regex=r"^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$",
    format_=strings["phone_number"]
)
