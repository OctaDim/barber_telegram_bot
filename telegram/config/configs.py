from dataclasses import dataclass
from typing import Literal, Union


@dataclass
class LANGUAGE_CONFIGS:
    LANGUAGE: Literal["EN", "RU"] = "EN"
    PHONE_NUMBER_REGION: Literal["BY", "RU", "US", "international"] = "BY"


@dataclass
class PAGINATION_CONFIGS:
    CATEGORIES_PER_PAGE: Union[int, 0] = 10  # 0 - show all categories without pages
    MASTERS_PER_PAGE: Union[int, 0] = 10  # 0 - show all categories without pages
    TIME_SLOTS_PER_PAGE: Union[int, 0] = 10  # 0 - show all categories without pages


@dataclass
class SERVICES_CONFIGS:
    SHOW_MASTERS_NAMES_WHEN_BY_CATEGORY: bool = True


@dataclass
class CALENDAR:
    SHOW_WEEKDAY_ICONS: bool = True
    WEEKDAYS_ABBR_UPPER_CASE: bool = False


@dataclass
class DB_SLOTS_CONFIGS:
    HIDE_SLOTS_OVER_TIME_LOSS_MAX_LIMIT: bool = True
    # 0 - hide all slots with time loss, very big (99999) - show all slots with time loss
    TIME_LOSS_MAX_LIMIT_FOR_HIDE_SLOTS: Union[int, 0] = 90  # In minutes

    MAKE_SPLIT_NEW_SLOTS_IF_TIME_LOSS: bool = True
    NEW_SLOT_FROM_TIME_LOSS_FOR_ADMIN_ONLY: bool = True
    # 0 - all slots will be split, very big (99999) - no one slot will be split
    MIN_TIME_LOSS_FOR_CREATING_NEW_SLOT: Union[int, 0] = 15  # In minutes


@dataclass
class SLOTS_CONFIGS:
    ONLY_TIME_START_UNIQUE_RANDOM_SLOTS: bool = False
    SHOW_SLOT_MASTER_FULL_NAME: bool = True
    SHOW_SAME_TIME_START_SLOT_NUMBER: bool = True
    SHOW_SAME_TIME_START_FIRST_SLOT_NUMBER: bool = True
    SHOW_SLOTS_ADVISES_ICONS: bool = True
    SHOW_SLOTS_ADVISING_ICON_HINT: bool = True
    MOST_ADVISED_TIME_LOSS_LIMIT: Union[int, 0] = 15  # In minutes. 0 to switch off diapason
    VERY_ADVISED_TIME_LOSS_LIMIT: Union[int, 0] = 30  # In minutes. 0 to switch off diapason
    ADVISED_TIME_LOSS_LIMIT: Union[int, 0] = 45  # In minutes. 0 to switch off diapason
    UNADVISED_TIME_LOSS_LIMIT: Union[int, 0] = 60  # In minutes. or 0 to switch off diapason
    # Very big number (99999) - all other slots except those diapasons above
    VERY_UNADVISED_TIME_LOSS_LIMIT: Union[int, 0] = 99999  # In minutes. 0 to switch off


@dataclass
class ENROLL_METHODS_CONFIGS:
    ENROLL_SERVICES_BY_CATEGORY: bool = True
    ENROLL_SERVICES_BY_CATEGORY_AND_MASTER: bool = True
    ENROLL_SERVICES_BY_MASTER: bool = True


@dataclass
class PAUSE_CONFIGS:
    LIST_DELAY: float | int | str = 0  # 0.2
    SHORT_MSG_DELAY: float | int | str = 3  # 2


@dataclass
class CONTACTS_CONFIGS:
    PHONES_INTERNATIONAL: bool = True
    DISABLE_PREVIEW: bool = True
