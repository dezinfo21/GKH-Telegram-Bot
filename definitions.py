""" Project definitions """
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

LOGS_DIR = os.path.join(ROOT_DIR, "logs")

LANGUAGE_FILE = "ru_RU.yaml"
LOCALIZATION_DIR = os.path.join(ROOT_DIR, "localization")

DATA_PATH = os.path.join(ROOT_DIR, "data.xlsx")
DATABASE_PATH = os.path.join(ROOT_DIR, "database.xlsx")
