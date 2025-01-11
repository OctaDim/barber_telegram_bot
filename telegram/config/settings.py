import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import dotenv_values

BASE_DIR = Path(__file__).resolve().parent.parent.parent
FULL_ENV_FILENAME = os.path.join(BASE_DIR, ".env")

environment_vars_dict = dotenv_values(FULL_ENV_FILENAME)


@dataclass
class BOT_CREDENTIALS:
    TG_BOT_TOKEN: str = environment_vars_dict.get("TG_BOT_TOKEN")

    TG_BOT_ADMINS_IDS: str = environment_vars_dict.get(
        "TG_BOT_ADMINS_IDS")

    TG_BOT_DEVELOPERS_IDS: str = environment_vars_dict.get(
        "TG_BOT_DEVELOPERS_IDS")

    BOT_START_STOP_MSG_IDS: str = environment_vars_dict.get(
        "BOT_START_STOP_MSG_IDS")
