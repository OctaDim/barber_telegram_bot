from dataclasses import dataclass


@dataclass
class ENROLL_METHODS_BUTTONS:
    ENROLL_MASTER_TO_SERVICE: str = "By Master"
    ENROLL_CATEGORY_TO_SERVICE: str = "By Category"
    ENROLL_CATEGORY_TO_MASTER: str = "By Category And Master"
    CONTINUE: str = "▶️ Continue"
