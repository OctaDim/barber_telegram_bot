from dataclasses import dataclass
from typing import Literal


@dataclass
class LANGUAGE_CONFIGS:
    LANGUAGE: Literal["EN", "RU"]= "EN"


@dataclass
class PAUSE_CONFIGS:
    LIST_DELAY: float|int|str = 0  # 0.2
    SHORT_MSG_DELAY: float|int|str = 2  # 2
