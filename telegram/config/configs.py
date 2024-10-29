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
    HIDE_SLOTS_MORE_TIME_LOSS_MAX_LIMIT: bool = False
    # 0 - hide all slots with time loss, very big (99999) - show all slots with time loss
    TIME_LOSS_MAX_LIMIT_FOR_HIDE_SLOTS: Union[int, 0] = 60  # In minutes

    MAKE_SPLIT_NEW_SLOTS_IF_TIME_LOSS: bool = True
    NEW_SLOT_FROM_TIME_LOSS_FOR_ADMIN_ONLY: bool = True
    # 0 - all slots will be split anyway, very big (99999) - no one slot will be split anyway
    MIN_TIME_LOSS_WHEN_CREATING_NEW_SLOT: Union[int, 0] = 15  # In minutes

@dataclass
class SLOTS_CONFIGS:
    SHOW_SLOTS_ADVISES: bool = True
    MOST_ADVISED_TIME_LOSS_LIMIT: Union[int, 0] = 15  # In minutes. 0 to switch off diapason
    VERY_ADVISED_TIME_LOSS_LIMIT: Union[int, 0] = 30  # In minutes. 0 to switch off diapason
    ADVISED_TIME_LOSS_LIMIT: Union[int, 0] = 45  # In minutes. 0 to switch off diapason
    UNADVISED_TIME_LOSS_LIMIT: Union[int, 0] = 60  # In minutes. or 0 to switch off diapason
    # Very big number (99999) - all other slots except those diapasons above
    VERY_UNADVISED_TIME_LOSS_LIMIT: Union[int, 0] = 99999  # In minutes. 0 to switch off


@dataclass
class PAUSE_CONFIGS:
    LIST_DELAY: float | int | str = 0  # 0.2
    SHORT_MSG_DELAY: float | int | str = 2  # 2


@dataclass
class CONTACTS_CONFIGS:
    PHONES_INTERNATIONAL: bool = True
    DISABLE_PREVIEW: bool = True
