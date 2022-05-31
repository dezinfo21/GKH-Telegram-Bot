import re
from dataclasses import dataclass, InitVar

from .abs_validator import AbstractValidator


@dataclass
class PhoneNumberValidator(AbstractValidator):
    regex: InitVar[str]

    def __post_init__(self, regex: str):
        self.pattern = re.compile(regex)

    async def validate(self, phone_number: str) -> bool:
        return bool(self.pattern.match(phone_number))


phone_number_validator = PhoneNumberValidator(
    regex=r"^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$",
    _format="Введите правильный росийский номер"
)
