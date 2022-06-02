""" Text validator """
from dataclasses import dataclass

from .abs_validator import AbstractValidator
from ..language import get_strings_sync


@dataclass
class TextValidator(AbstractValidator):
    """
    Validator for text

    Attributes:
        min_len (int): minimum length for text
        max_len (int): maximum length for text
    """
    min_len: int
    max_len: int

    async def validate(self, text: str) -> bool:
        return self.min_len < len(text) < self.max_len


strings = get_strings_sync(module="valid_formats")

text_validator = TextValidator(
    min_len=32,
    max_len=2048,
    format_=strings["text"]
)
