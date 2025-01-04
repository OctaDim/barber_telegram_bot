from dataclasses import dataclass


@dataclass
class SERVICES_BUTTONS:
    ENROLL_SINGLE_MASTER_SERVICES = "✍️ Записаться к мастеру"  # Must be unique among inline and reply buttons!!!
    ENROLL_SERVICES = "✍️ Записаться на услуги"  # Must be unique among inline and reply buttons!!!
    MY_RESERVATIONS = "✅ Мои записи"
    OUR_SERVICES = "✂️ Наши услуги"
    OUR_PROMOTIONS = "🔥 Акции"
