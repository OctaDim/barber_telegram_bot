from dataclasses import dataclass
from datetime import timedelta


@dataclass
class BUTTONS_CHANGE_SERVICES:
    NAME: str = "Название"
    DESCRIPTION: str = "Описание"
    PRICE: str = "Цена"
    DURATION: str = "Продолжительность"
