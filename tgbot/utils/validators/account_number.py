import re
from dataclasses import dataclass, InitVar

from .abs_validator import AbstractValidator


@dataclass
class AccountNumberValidator(AbstractValidator):
    regex: InitVar[str]

    def __post_init__(self, regex: str):
        self.pattern = re.compile(regex)

    async def validate(self, account_number: str) -> bool:
        return bool(self.pattern.match(account_number))


account_number_validator = AccountNumberValidator(
    regex=r"^\d{5}$",
    _format="Введите правильный номер лицевого счета"
)
