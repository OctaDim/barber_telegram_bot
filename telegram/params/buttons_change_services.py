from dataclasses import dataclass
from datetime import timedelta


@dataclass
class BUTTONS_CHANGE_SERVICES:
    NAME: str = "Name"
    DESCRIPTION: str = "Description"
    PRICE: str = "Price"
    DURATION: str = "Time duration"
