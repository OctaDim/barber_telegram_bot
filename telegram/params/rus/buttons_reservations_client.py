from dataclasses import dataclass


@dataclass
class RESERVATIONS_BUTTONS:
    PAGE: str = "Стр"
    CANCEL_RESERVATION: str = "🚫 Отменить"
    COMPLETED_RESERVATION: str = "🔆 Выполнено"
    CANCELLED_BY_USER: str = "❄️ Отменено клиентом"
    CANCELLED_BY_ADMIN: str = "❄️ Отменено админом"
    CANCEL_RESERVATION_YES: str = "ДА"
    CANCEL_RESERVATION_NO: str = "НЕТ"
