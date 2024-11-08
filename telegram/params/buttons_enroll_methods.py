from dataclasses import dataclass


@dataclass
class ENROLL_METHODS_BUTTONS:
    ENROLL_CATEGORY_TO_MASTER: str = "Category and Master"
    ENROLL_MASTER_TO_SERVICE: str = "Master"
    ENROLL_CATEGORY_TO_SERVICE: str = "Category"
    CONTINUE: str = "▶️ Continue"
