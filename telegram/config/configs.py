from dataclasses import dataclass
from typing import Literal, Union


@dataclass
class LANGUAGE_CONFIGS:
    LANGUAGE: Literal["EN", "RU"] = "EN"
    PHONE_NUMBER_REGION: Literal["BY", "RU", "US", "international"] = "BY"


@dataclass
class PAGINATION_CONFIGS:
    CATEGORIES_PER_PAGE: Union[int, 0] = 7  # 0 - show all categories without pages
    MASTERS_PER_PAGE: Union[int, 0] = 7  # 0 - show all categories without pages
    TIME_SLOTS_PER_PAGE: Union[int, 0] = 7  # 0 - show all categories without pages
    RESERVATIONS_PER_PAGE: Union[int, 0] = 7  # 0 - show all categories without pages


@dataclass
class SERVICES_CONFIGS:
    SHOW_MASTERS_NAMES_WHEN_BY_CATEGORY: bool = True
    SHOW_CANCEL_ALL_SERVICES_BUTTON: bool = False


@dataclass
class CALENDAR_CONFIGS:
    SHOW_WEEKDAY_ICONS: bool = True
    WEEKDAYS_ABBR_UPPER_CASE: bool = False
    MONTH_NAME_UPPER_CASE: bool = True
    MONTH_AND_YEAR_IN_ONE_BUTTON: bool = True


@dataclass
class DB_SLOTS_CONFIGS:
    HIDE_SLOTS_OVER_TIME_LOSS_MAX_LIMIT: bool = True
    # 0 - hide any time loss slots, very big (99999) - show all slots (incl any time loss)
    TIME_LOSS_MAX_LIMIT_FOR_HIDE_SLOTS: Union[int, 0] = 90  # In minutes

    MAKE_SPLIT_NEW_SLOTS_IF_TIME_LOSS: bool = True
    NEW_SLOT_FROM_TIME_LOSS_FOR_ADMIN_ONLY: bool = True
    # 0 - all slots will be split, very big (99999) - no one slot will be split
    MIN_TIME_LOSS_FOR_CREATING_NEW_SLOT: Union[int, 0] = 15  # In minutes


@dataclass
class SLOTS_CONFIGS:
    ONLY_TIME_START_UNIQUE_RANDOM_SLOTS: bool = False
    SHOW_SLOT_MASTER_FULL_NAME: bool = True
    SHOW_SAME_TIME_START_SLOT_NUMBER: bool = False
    SHOW_SAME_TIME_START_FIRST_SLOT_NUMBER: bool = True
    SHOW_SLOTS_ADVISES_ICONS: bool = True
    SHOW_SLOTS_ADVISING_ICON_HINT: bool = True
    POINTS_5_TIME_LOSS_LIMIT: Union[int, 0] = 0  # In minutes. 0 to switch off diapason
    POINTS_4_TIME_LOSS_LIMIT: Union[int, 0] = 0  # In minutes. 0 to switch off diapason
    POINTS_3_TIME_LOSS_LIMIT: Union[int, 0] = 25  # In minutes. 0 to switch off diapason
    POINTS_2_TIME_LOSS_LIMIT: Union[int, 0] = 45  # In minutes. or 0 to switch off diapason
    # Very big number (99999) - all other slots except those diapasons above
    POINTS_1_TIME_LOSS_LIMIT: Union[int, 0] = 99999  # In minutes. 0 to switch off


@dataclass
class ENROLL_METHODS_CONFIGS:
    ENROLL_SINGLE_MASTER_SERVICES: bool = True
    ENROLL_SERVICES_BY_CATEGORY_AND_MASTER: bool = True
    ENROLL_SERVICES_BY_CATEGORY: bool = True
    ENROLL_SERVICES_BY_MASTER: bool = True
    ENROLL_SERVICES_BY_SERVICES: bool = True


@dataclass
class RESERVATIONS_CONFIGS:
    SHOW_COMPLETED_RESERVATIONS: bool = True
    SHOW_RESERVATIONS_CLIENT_CANCELLED: bool = True
    SHOW_RESERVATIONS_ADMIN_CANCELLED: bool = True


@dataclass
class PAUSE_CONFIGS:
    LIST_MESSAGES_COMMON_DELAY: float | int | str = 0  # 0 default, 0 - switch off delay
    LIST_MORE_30_MESSAGES_DELAY: float | int | str = 0.05  # 0.1 default, 0 - switch off delay
    INFO_MESSAGE_DELAY: float | int | str = 5  # 5
    WARNING_MESSAGE_DELAY: float | int | str = 10  # 10


@dataclass
class CONTACTS_CONFIGS:
    PHONES_INTERNATIONAL: bool = True
    DISABLE_PREVIEW: bool = True
