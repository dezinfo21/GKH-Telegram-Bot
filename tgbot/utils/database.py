""" Database module """
import functools
import logging
import re
from datetime import datetime
from typing import NamedTuple, Callable

import pandas as pd

from definitions import DATABASE_PATH, DATA_PATH

log = logging.getLogger(__name__)

SHEETS = {
    "main_info": {
        "name": "Основная информация",
        "columns": {
            "A": "Идентификатор лицевого счета",
            "B": "Номер ЛС",
            "C": "Идентификатор ЖКУ",
            "D": "Тип платежного документа",
            "E": "Форма платежного документа",
            "F": "Идентификатор платежного документа",
            "G": "Номер платежного документа",
            "H": "Статус платежного документа",
            "I": "Расчетный период\n(ММ.ГГГГ)",
            "J": "Сумма к оплате за расчетный период, руб. (по всему платежному документу)",
            "M": "Оплачено денежных средств, руб.",
            "O": "Дата последней поступившей оплаты",
            "Q": "Итого к оплате за расчетный период c учетом задолженности/переплаты, руб. (по всему платежному документу)",
            "S": "ИТОГО К ОПЛАТЕ (по всем услугам)",
            "Z": "Дата размещения"
        }
    },
    "addresses": {
        "name": "Адрес плательщика",
        "columns": {
            "C": "Адрес ОЖФ"
        }
    },
    "users": {
        "name": "Пользователи",
        "columns": {
            "A": "Телеграм ID",
            "B": "Номер телефона",
            "C": "Номер ЛС",
            "D": "Номер квартиры",
            "E": "ФИО"
        }
    }
}


class UserModel(NamedTuple):
    """
    User model

    Attributes:
        user_id (int):
        phone_number (int):
        account_number (int):
        flat_number (int):
        full_name (str):
    """

    user_id: int
    phone_number: int
    account_number: int
    flat_number: int
    full_name: str


class ContactInfoModel(NamedTuple):
    """
    Contact information model

    Attributes:
        flat_number (int):
        phone_number (int):
        full_name (str):
        date (str):
        text (str):
    """

    flat_number: int
    phone_number: int
    full_name: str
    date: str
    text: str


class BidModel(NamedTuple):
    """
    Bid model

    Attributes:
        flat_number (int):
        phone_number (int):
        full_name (str):
        date (str):
        text (str):
    """

    flat_number: int
    phone_number: int
    full_name: str
    date: str
    text: str


class DebtModel(NamedTuple):
    """
    Debt model

    Attributes:
        billing_period (str): due date to pay
        last_payment_date (datetime): last payment date
        placement_date (datetime): date the application was placed
        money_paid (float): amount that was paid
        money_sum_with_debt (float): amount to be paid
    """

    billing_period: str
    last_payment_date: datetime
    placement_date: datetime
    money_paid: float
    money_sum_with_debt: float


def _check_duplicate(phone_number: int, account_number: int) -> bool | None:
    """
    Check whether user with same phone number and account number is already exists
    Args:
        phone_number (str):
        account_number (int):

    Returns:
        bool: True if user is already exists, otherwise False
    """
    try:
        df = pd.read_excel(
            DATABASE_PATH,
            sheet_name=SHEETS["users"]["name"],
            engine="openpyxl",
            usecols=[
                SHEETS["users"]["columns"]["B"],
                SHEETS["users"]["columns"]["C"]
            ]
        )

        user_info = df.loc[
            (df[SHEETS["users"]["columns"]["B"]] == phone_number) &
            (df[SHEETS["users"]["columns"]["C"]] == account_number)
            ]
    except Exception:
        log.exception(f"Exception while checking user with account [{phone_number=}] and [{account_number=}] "
                      f"for duplicate")
        return None
    else:
        return not user_info.empty


def _get_flat_num(address: str) -> int:
    """
    Get flat number from full address

    Args:
        address (str): full user's address

    Returns:
        int: flat number

    Examples:
        Татарстан Респ, г. Казань, ул. Халева, д. 7, кв. 45 -> 45
        Татарстан Респ, г. Казань, ул. Халева, д. 7, кв. 46 -> 46
        Татарстан Респ, г. Казань, ул. Халева, д. 7, кв. 31 -> 31
    """
    return int(re.search(r"кв. \d+", address).group().split()[1])


def _format_account_num(account_number: float) -> str:
    """
    Get the last 5 characters of account number

    Args:
        account_number (float): full account number

    Returns:
        str: last 5 characters of account number

    Examples:
        123456789876.0 -> '78987'
        435634545657.0 -> '45657'
        636765836264.0 -> '36264'
    """

    return str(int(account_number))[-5:]


def _format_phone_number(phone_number: str) -> int:
    """
    Format denormalized rus phone number into normalized

    Args:
        phone_number (str): denormalized rus phone number

    Returns:
        int: normalized rus phone number

    Examples:
        +79999999999 -> 79999999999
        89999999999 -> 79999999999
        7 (999) 99 9 99 9 9 -> 79999999999
    """
    norm_phone_number = (
        phone_number.replace(" ", "").replace("-", "").replace("(", "").replace(")", "").replace("+", "")[1:]
    )

    return int(f"7{norm_phone_number}")


def _create_new_user(
        user_id: int,
        flat_number: int,
        phone_number: str,
        account_number: str,
        full_name: str
) -> pd.DataFrame | None:
    """
    Create new user

    Args:
        user_id (int): user's telegram id
        flat_number (int): flat number
        phone_number (str): denormalized rus phone number
        account_number (str): denormalized account number
        full_name (str): user's full name

    Returns:
        pd.DataFrame if user was created successfully, otherwise None
    """
    try:
        df = pd.read_excel(
            DATA_PATH,
            sheet_name=[SHEETS["main_info"]["name"], SHEETS["addresses"]["name"]],
            engine="openpyxl"
        )

        account_numbers = df[SHEETS["main_info"]["name"]].loc[1:, SHEETS["main_info"]["columns"]["B"]]
        addresses = df[SHEETS["addresses"]["name"]].loc[:, SHEETS["addresses"]["columns"]["C"]]
    except Exception:
        log.exception(f"Error while creating user with [{user_id=}]")
        return None

    for full_acc_num, address in zip(account_numbers, addresses):
        norm_flat_num = _get_flat_num(address)
        norm_acc_num = _format_account_num(full_acc_num)

        if norm_acc_num != account_number and norm_flat_num != flat_number:
            continue

        phone_num = _format_phone_number(phone_number)

        if _check_duplicate(phone_num, full_acc_num):
            return None

        new_user = pd.DataFrame(
            data=[
                user_id,
                phone_num,
                full_acc_num,
                norm_flat_num,
                full_name
            ],
            columns=[
                SHEETS["users"]["columns"]["A"],
                SHEETS["users"]["columns"]["B"],
                SHEETS["users"]["columns"]["C"],
                SHEETS["users"]["columns"]["D"],
                SHEETS["users"]["columns"]["E"]
            ]
        )

        return new_user


def save_user(
        user_id: int,
        flat_number: int,
        phone_number: str,
        account_number: str,
        full_name: str
) -> bool:
    """
    Save new user into exel database

    Args:
        user_id (int): user's telegram id
        flat_number (int): flat number
        phone_number (str): denormalized rus phone number
        account_number (str): denormalized account number
        full_name (str): user's full name

    Returns:
        bool: True if user was successfully saved, otherwise False
    """
    new_user = _create_new_user(user_id, flat_number, phone_number, account_number, full_name)

    if new_user is None:
        return False

    try:
        df = pd.read_excel(
            DATABASE_PATH,
            sheet_name=SHEETS["users"]["name"],
            engine="openpyxl"
        )

        new_df = pd.concat([df, new_user])

        with pd.ExcelWriter(DATABASE_PATH) as writer:
            new_df.to_excel(writer, SHEETS["users"]["name"], index=False)
    except Exception:
        log.exception(f"Error while saving user with [{user_id=}]")
        return False
    else:
        return True


async def get_user(user_id: int) -> UserModel | None:
    """
    Get user from database by user id

    Args:
        user_id (int): user's telegram id

    Returns:
        UserModel: if user exists, otherwise None
    """
    df = pd.read_excel(
        DATABASE_PATH,
        sheet_name=SHEETS["users"]["name"],
        engine="openpyxl"
    )

    user_df = df.loc[df[SHEETS["users"]["columns"]["A"]] == user_id]

    if user_df.empty:
        return None

    user_info = user_df.to_dict(orient="records")[0]

    return UserModel(
        user_info[SHEETS["users"]["columns"]["A"]],
        user_info[SHEETS["users"]["columns"]["B"]],
        user_info[SHEETS["users"]["columns"]["C"]],
        user_info[SHEETS["users"]["columns"]["D"]],
        user_info[SHEETS["users"]["columns"]["E"]]
    )


async def get_user_debt(account_number: int) -> DebtModel:
    df = pd.read_excel(
        DATA_PATH,
        sheet_name=SHEETS["main_info"]["name"],
        usecols=[
            SHEETS["main_info"]["columns"]["B"],
            SHEETS["main_info"]["columns"]["I"],
            SHEETS["main_info"]["columns"]["M"],
            SHEETS["main_info"]["columns"]["O"],
            SHEETS["main_info"]["columns"]["Q"],
            SHEETS["main_info"]["columns"]["Z"]
        ],
        engine="openpyxl"
    )

    df[SHEETS["main_info"]["columns"]["O"]] = df[SHEETS["main_info"]["columns"]["O"]].dt.strftime("%d.%m.%Y")
    df[SHEETS["main_info"]["columns"]["Z"]] = df[SHEETS["main_info"]["columns"]["Z"]].dt.strftime("%d.%m.%Y")

    user_info = df.loc[df[SHEETS["main_info"]["columns"]["B"]] == account_number].to_dict(orient="records")[0]

    placement_date = user_info[SHEETS["main_info"]["columns"]["Z"]]
    billing_period = str(user_info[SHEETS["main_info"]["columns"]["I"]])
    last_payment_date = user_info[SHEETS["main_info"]["columns"]["O"]]

    money_sum_with_debt = user_info[SHEETS["main_info"]["columns"]["Q"]]
    money_paid = user_info[SHEETS["main_info"]["columns"]["M"]]

    return DebtModel(
        billing_period,
        last_payment_date,
        placement_date,
        money_paid,
        money_sum_with_debt
    )


def get_user_decorator(user_id: int) -> Callable:
    """
    Decorator to get UserModel object instance in function

    Args:
        user_id (int): user's telegram id

    Returns:
        UserModel | None: Decorated function with UserModel object instance
        if user with user id exists else decorated function with None
    """
    def decorate(func):
        @functools.wraps(func)
        async def wrapped(*args, **kwargs):
            user = await get_user(user_id)
            return await func(*args, user, **kwargs)

        return wrapped

    return decorate
