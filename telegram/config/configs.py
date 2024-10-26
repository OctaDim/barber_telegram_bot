from dataclasses import dataclass
from typing import Literal, Union


@dataclass
class LANGUAGE_CONFIGS:
    LANGUAGE: Literal["EN", "RU"] = "EN"
    PHONE_NUMBER_REGION: Literal["BY", "RU", "US", "international"] = "international"


@dataclass
class CALENDAR:
    SHOW_WEEKDAY_ICONS: bool = True
    WEEKDAYS_ABBR_UPPER_CASE: bool = False


@dataclass
class DB_SLOTS_CONFIGS:
    LIMIT_SLOTS_BY_TIME_LOSS: bool = False
    SLOT_TIME_LOSS_MAX_LIMIT: Union[int, None, 0] = 90  # In minutes. None or 0 to switch off


@dataclass
class SLOTS_CONFIGS:
    SHOW_SLOTS_ADVISES: bool = True
    MOST_ADVISED_TIME_LOSS_LIMIT: Union[int, None, 0] = 15  # In minutes. None or 0 to switch off
    VERY_ADVISED_TIME_LOSS_LIMIT: Union[int, None, 0] = 30  # In minutes. None or 0 to switch off
    ADVISED_TIME_LOSS_LIMIT: Union[int, None, 0] = 45  # In minutes. None or 0 to switch off
    UNADVISED_TIME_LOSS_LIMIT: Union[int, None, 0] = 60  # In minutes. None or 0 to switch off
    # All others. Very big number should be, ex. 99999
    VERY_UNADVISED_TIME_LOSS_LIMIT: Union[int, None, 0] = 999999  # In minutes. None or 0 to switch off


@dataclass
class PAUSE_CONFIGS:
    LIST_DELAY: float | int | str = 0  # 0.2
    SHORT_MSG_DELAY: float | int | str = 2  # 2


@dataclass
class CONTACTS_CONFIGS:
    PHONES_INTERNATIONAL: bool = True
    DISABLE_PREVIEW: bool = True
