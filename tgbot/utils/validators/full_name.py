import re
from dataclasses import dataclass, InitVar

from .abs_validator import AbstractValidator


@dataclass
class FullNameValidator(AbstractValidator):
    regex: InitVar[str]

    def __post_init__(self, regex: str):
        self.pattern = re.compile(regex)

    async def validate(self, full_name: str) -> bool:
        return bool(self.pattern.match(full_name))


full_name_validator = FullNameValidator(
    regex=r"^[\w-]{3,48}\s[\w-]{3,48}\s[\w-]{3,48}$",
    _format="Введите правильные ФИО, в формате Петров Петр Петрович."
)
