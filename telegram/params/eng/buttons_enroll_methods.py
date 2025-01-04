from dataclasses import dataclass


@dataclass
class ENROLL_METHODS_BUTTONS:
    ENROLL_CATEGORY_TO_MASTER: str = "by Category and Master"
    ENROLL_MASTER_TO_SERVICE: str = "by Master"
    ENROLL_CATEGORY_TO_SERVICE: str = "by Category"
    ENROLL_SERVICES_DIRECTLY: str = "by Services"
    CONTINUE: str = "▶️ Continue"
