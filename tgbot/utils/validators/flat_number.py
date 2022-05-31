from dataclasses import dataclass

from .abs_validator import AbstractValidator


@dataclass
class FlatNumberValidator(AbstractValidator):
    min_value: int
    max_value: int

    async def validate(self, flat_number_str: str) -> bool:
        try:
            flat_number = int(flat_number_str)
        except ValueError:
            return False

        return self.min_value < flat_number < self.max_value


flat_number_validator = FlatNumberValidator(
    min_value=0,
    max_value=10000,
    _format="Введите праввильный номер квартиры"
)
