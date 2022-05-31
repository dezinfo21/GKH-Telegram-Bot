""" Language module """
import functools
import logging
import os
import sys
from dataclasses import dataclass
from typing import Callable, NoReturn

import yaml
from babel.core import Locale

from definitions import LANGUAGE_FILE, LOCALIZATION_DIR
from tgbot.data.config import load_config

log = logging.getLogger(__name__)
config = load_config(".env")

LANGUAGE = {}


@dataclass
class Strings:
    """
    Implements the interface for working with strings in the language specified in the config

    Attributes:
        module (str): default module in master from which strings are needed
        mas_name (str): default master  in LANGUAGES
    """

    module: str
    mas_name: str

    @staticmethod
    def get_strings(mas_name_: str, module_: str) -> dict:
        """
        Get all strings contained in LANGUAGE -> mas_name_ -> module_name_

        Args:
            module_ (str): module in master from which strings are needed
            mas_name_ (str): master in LANGUAGES

        Raises:
            KeyError: if mas_name_ not in LANGUAGE or module_ not in LANGUAGE -> mas_name_

        Returns:
            dict: all strings contained in LANGUAGE -> mas_name_ -> module_

        Examples:
            LANGUAGE:
                -language_info:
                    -flag: *
                    -code: ru
                    -babel: Locale('ru')
                -STRINGS:
                    -welcome:
                        -welcome1: hello1
                        -welcome2: hello2
                    -start:
                        -start1: start1
                        -start2: start2

            LANGUAGE -> module_ -> mas_name_
            LANGUAGE -> STRINGS -> welcome
        """
        if mas_name_ not in LANGUAGE:
            raise KeyError(f"There is now '{mas_name_}' in 'LANGUAGE'")

        if module_ not in LANGUAGE[mas_name_]:
            raise KeyError(f"There is now '{module_}' in 'LANGUAGE' -> '{mas_name_}'")

        data = LANGUAGE[mas_name_][module_]

        if mas_name_ == "STRINGS":
            data["language_info"] = LANGUAGE["language_info"]

        return data

    def get_string(self, string_name) -> str:
        """
        Get string from LANGUAGE -> mas_name -> module_name

        Args:
            string_name (str): string to return

        Raises:
            KeyError: if string_name not in LANGUAGE -> mas_name -> module_name

        Returns:
            str: string from LANGUAGE -> mas_name -> module_name

        Examples:
            LANGUAGE:
                -language_info:
                    -flag: *
                    -code: ru
                    -babel: Locale('ru')
                -STRINGS:
                    -welcome:
                        -welcome1: hello1
                        -welcome2: hello2
                    -start:
                        -start1: start1
                        -start2: start2

            LANGUAGE -> mas_name -> module_name -> string_name
            LANGUAGE -> STRINGS -> start -> start1
        """
        data = self.get_strings(self.mas_name, self.module)

        if string_name not in data:
            raise KeyError(f"There is not '{string_name}' in 'LANGUAGE' -> '{self.mas_name}' -> '{self.module}'")

        return data[string_name]

    def __getitem__(self, key) -> str:
        return self.get_string(key)


async def get_strings(module: str, mas_name: str = "STRINGS") -> Strings:
    """
    Create and return _Strings object instance

    Args:
        module (str): module in master from which strings are needed
        mas_name (str): (default=STRINGS) master in LANGUAGES

    Returns:
        _Strings object instance
    """
    return Strings(module, mas_name)


async def get_string(module_name: str, string_name: str, mas_name: str = "STRINGS"):
    """
    Get a string from LANGUAGE -> mas_name -> module_name

    Args:
        module_name (str): module in master from which strings are needed
        string_name (str): string to find in module
        mas_name (str): master in LANGUAGES

    Returns:
        str: string from LANGUAGE -> mas_name -> module_name if it exists
    """
    strings = await get_strings(module_name, mas_name)
    return strings[string_name]


def get_strings_decorator(module: str, mas_name: str = "STRINGS") -> Callable:
    """
    Decorator to get _Strings object instance in function

    Args:
        module (str): module in master from which strings are needed
        mas_name (str): master in which to find module

    Returns:
        Decorated function with _Strings object instance
    """
    def decorate(func):
        @functools.wraps(func)
        async def wrapped(*args, **kwargs):
            strings = await get_strings(module, mas_name)
            return await func(*args, strings, **kwargs)

        return wrapped

    return decorate


def setup() -> NoReturn:
    """
    Setup localization

    Returns:
        NoReturn
    """
    log.info("Configure localizations...")
    path = os.path.join(LOCALIZATION_DIR, LANGUAGE_FILE)

    if os.path.exists(path):
        with open(path, "r", encoding="utf8") as f:
            lang = yaml.load(f, Loader=yaml.CLoader)

            lang_code = lang['language_info']['code']
            lang['language_info']['babel'] = Locale(lang_code)

            global LANGUAGE
            LANGUAGE = lang

    else:
        sys.exit(log.critical(f"Unable to find language file '{LANGUAGE_FILE}' in '{LOCALIZATION_DIR}'"))
