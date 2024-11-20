from dataclasses import dataclass


@dataclass
class RESERVATIONS_BUTTONS:
    PAGE: str = "PAGE"
    CANCEL_RESERVATION: str = "Cancel"
    COMPLETED_RESERVATION: str = "🔆 Completed"
    CANCELLED_BY_USER: str = "❄️ Cancelled"
    CANCELLED_BY_ADMIN: str = "❄️ Cancelled"
