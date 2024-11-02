from dataclasses import dataclass


@dataclass
class ENROLL_METHODS_BUTTONS:
    ENROLL_BY_MASTER: str = "By Master"
    ENROLL_BY_CATEGORY: str = "By Category"
    ENROLL_BY_CATEGORY_AND_MASTER: str = "By Category And Master"
