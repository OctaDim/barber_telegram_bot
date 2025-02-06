from dataclasses import dataclass


@dataclass
class ENROLL_SRCS_BUTTONS:
    ENROLL_SERVICE: str = "☝️ Записаться"
    CANCEL_SERVICE: str = "🚫 Отменить запись"
    ENROLL_ONE_MORE: str = "✅️+1  Ещё раз"
    CANCEL_ALL_SERVICES: str = "⏹ Отменить эту услугу"
    # IMPORTANT: Two spaces or special symbol to be unique among inl and reply buttons!!!
    RETURN_TO_MASTERS: str = "↩️  Вернуться"  # Two spaces after icon to be unique!!!
    CONTINUE_ENROLL_SERVICES: str = "🟢 ПРОДОЛЖИТЬ ЗАПИСЬ НА УСЛУГИ"
