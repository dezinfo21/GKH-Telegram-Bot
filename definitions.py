""" Project definitions """
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

LOGS_DIR = os.path.join(ROOT_DIR, "logs")
TGBOT_DIR = os.path.join(ROOT_DIR, "tgbot")

LANGUAGE_FILE = "ru_RU.yaml"
LOCALIZATION_DIR = os.path.join(ROOT_DIR, "localization")

DATA_PATH = os.path.join(TGBOT_DIR, "data", "data.xlsx")
DATABASE_PATH = os.path.join(TGBOT_DIR, "data", "database.xlsx")
PRICE_LIST_PATH = os.path.join(TGBOT_DIR, "data", "price_list.xlsx")
