""" Account number validator """
import re
from dataclasses import dataclass, InitVar

from tgbot.utils.language import get_strings_sync
from .abs_validator import AbstractValidator


@dataclass
class AccountNumberValidator(AbstractValidator):
    """
    Validator for account number

    Attributes:
        regex (InitVar[str]): regular expression for pattern,
        which will be used to validate account number
    """
    regex: InitVar[str]

    def __post_init__(self, format_: str, regex: str):
        self._format = format_
        self.pattern = re.compile(regex)

    async def validate(self, account_number: str) -> bool:
        return bool(self.pattern.match(account_number))


strings = get_strings_sync(module="valid_formats")

account_number_validator = AccountNumberValidator(
    regex=r"^\d{5}$",
    format_=strings["account_number"]
)
