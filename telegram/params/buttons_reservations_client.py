from dataclasses import dataclass


@dataclass
class RESERVATIONS_BUTTONS:
    PAGE: str = "Стр"
    CANCEL_RESERVATION: str = "❎ Отменить"
    COMPLETED_RESERVATION: str = "Завершено"
    CANCELLED_BY_USER: str = "Отм клиентом"
    CANCELLED_BY_ADMIN: str = "Отм админом"
    CANCEL_RESERVATION_YES: str = "ДА"
    CANCEL_RESERVATION_NO: str = "НЕТ"
