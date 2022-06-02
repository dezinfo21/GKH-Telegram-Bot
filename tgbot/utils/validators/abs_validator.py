""" Abstract validator """
import abc
from dataclasses import dataclass, InitVar


@dataclass
class AbstractValidator(abc.ABC):
    """
    Abstract validator

    Attributes:
        format_ (InitVar[str]): message, which will be showed if validation failed
    """
    format_: InitVar[str]

    def __post_init__(self, format_: str):
        self._format = format_

    @abc.abstractmethod
    async def validate(self, value: str) -> bool:
        """
        Validate entered value
        Should be overwritten by children class

        Args:
            value (str):

        Returns:
            bool: True if value is valid, otherwise False
        """
        raise NotImplementedError("Validate method should be overwritten")

    @property
    def valid_format(self) -> str:
        """
        Property to return valid format for entered message

        Returns:
            str: valid format for value
        """
        return self._format
