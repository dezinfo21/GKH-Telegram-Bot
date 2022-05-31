from dataclasses import dataclass

from .abs_validator import AbstractValidator


@dataclass
class TextValidator(AbstractValidator):
    min_len: int
    max_len: int

    async def validate(self, text: str) -> bool:
        return self.min_len < len(text) < self.max_len


text_validator = TextValidator(
    min_len=32,
    max_len=2048,
    _format="Текст сообщения должен быть не меньше 32 символов и не больше 2048 символов."
)
