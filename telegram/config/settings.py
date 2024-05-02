import os
from pathlib import Path
from dotenv import dotenv_values
from dataclasses import dataclass

BASE_DIR = Path(__file__).resolve().parent.parent.parent
FULL_ENV_FILENAME = os.path.join(BASE_DIR, ".env")

environment_vars_dict = dotenv_values(FULL_ENV_FILENAME)


@dataclass
class BOT_CREDENTIALS:
    TG_BOT_NAME: str = environment_vars_dict.get("TG_BOT_NAME")
    TG_BOT_USERNAME: str = environment_vars_dict.get("TG_BOT_USERNAME")
    TG_BOT_URL: str = environment_vars_dict.get("TG_BOT_URL")
    TG_BOT_TOKEN: str = environment_vars_dict.get("TG_BOT_TOKEN")



# import os
# from pathlib import Path
# from dotenv import dotenv_values
# from dataclasses import dataclass
#
# BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
# FULL_ENV_FILENAME = os.path.join(BASE_DIR, ".env")
#
# environment_vars_dict = dotenv_values(FULL_ENV_FILENAME)
#
#
# @dataclass
# class BOT_CREDENTIALS:
#     TG_BOT_NAME: str = environment_vars_dict.get("TG_BOT_NAME")
#     TG_BOT_USERNAME: str = environment_vars_dict.get("TG_BOT_USERNAME")
#     TG_BOT_URL: str = environment_vars_dict.get("TG_BOT_URL")
#     TG_BOT_TOKEN: str = environment_vars_dict.get("TG_BOT_TOKEN")
#
#
# print(BOT_CREDENTIALS.TG_BOT_TOKEN)
