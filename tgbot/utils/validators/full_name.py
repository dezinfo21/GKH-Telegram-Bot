""" Full name validator """
import re
from dataclasses import dataclass, InitVar

from .abs_validator import AbstractValidator
from ..language import get_strings_sync


@dataclass
class FullNameValidator(AbstractValidator):
    """
    Validator for full name

    Attributes:
        regex (InitVar[str]): regular expression for pattern,
        which will be used to validate value
    """
    regex: InitVar[str]

    def __post_init__(self, format_: str, regex: str):
        self._format = format_
        self.pattern = re.compile(regex)

    async def validate(self, full_name: str) -> bool:
        return bool(self.pattern.match(full_name))


strings = get_strings_sync(module="valid_formats")

full_name_validator = FullNameValidator(
    regex=r"^[\w-]{3,48}\s[\w-]{3,48}\s[\w-]{3,48}$",
    format_=strings["full_name"]
)
