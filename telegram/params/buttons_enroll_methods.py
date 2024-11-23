from dataclasses import dataclass


@dataclass
class ENROLL_METHODS_BUTTONS:
    ENROLL_CATEGORY_TO_MASTER: str = "by category and master"
    ENROLL_MASTER_TO_SERVICE: str = "by master"
    ENROLL_CATEGORY_TO_SERVICE: str = "by category"
    CONTINUE: str = "▶️ Continue"
