import inspect
import locale
import platform
from typing import Literal


def get_system_locale_name(
        language: Literal["EN", "US", "HE-IL", "RU"] = "EN"
) -> str | None:
    print(f"{'-' * 115}\n\tFunction: {inspect.currentframe().f_code.co_name}\n")

    if platform.system() == "Windows":
        match language:
            case "US":
                locale_name = "en_US"
                # locale_name = "English_United States.1252"
            case "RU":
                locale_name = "ru_RU"
                # locale_name = "Russian_Russia.1251"
            case "HE-IL":
                # locale_name = "he_IL"
                locale_name = "Hebrew_Israel.1255"
            case "EN" | _:
                locale_name = ""
    elif platform.system() == "Linux":
        match language:
            case "RU":
                locale_name = "ru_RU.UTF-8"
            case "HE-IL":
                locale_name = "he_IL.UTF-8"
            case "US":
                locale_name = "en_US.UTF-8"
            case "EN" | _:
                locale_name = ""
    else:
        locale_name = ""

    print(f"\tLocale name got: \n"
          f"\tlanguage = '{language}'\n"
          f"\tlocale_name = '{locale_name}'\n")

    return locale_name


def set_system_locale_name(locale_name: str = None) -> None:
    print(f"{'-' * 115}\n\tFunction: {inspect.currentframe().f_code.co_name}\n")

    if not locale_name:
        print(f"\tLocale was not set because "
              f"\tlocale_name = '{locale_name}'\n")
        return

    try:
        locale.setlocale(locale.LC_TIME, locale=locale_name)
        print(f"\tLocale set successfully:\n"
              f"\tlocale_name = '{locale_name}'\n")
    except (locale.Error, ValueError, Exception) as locale_error:
        print(f"\tLocale was not set because "
              f"\tlocale_error = {locale_error}\n"
              f"\tlocale_name = '{locale_name}'\n")
