from dataclasses import dataclass


@dataclass
class ENROLL_METHODS_BUTTONS:
    ENROLL_CATEGORY_TO_MASTER: str = "по Категории и Мастеру"
    ENROLL_MASTER_TO_SERVICE: str = "по Мастеру"
    ENROLL_CATEGORY_TO_SERVICE: str = "по Категории"
    ENROLL_SERVICES_DIRECTLY: str = "по Услугам"
    CONTINUE: str = "▶️ Продолжить"
