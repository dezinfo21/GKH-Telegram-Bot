import abc
from dataclasses import dataclass


@dataclass
class AbstractValidator(abc.ABC):
    _format: str

    @abc.abstractmethod
    async def validate(self, value: str) -> bool:
        ...

    @property
    def valid_format(self) -> str:
        return self._format
