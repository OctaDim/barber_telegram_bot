from dataclasses import dataclass
from telegram.params.buttons_common import COMMON_BUTTONS_PARAMS



@dataclass
class MAIN_MENU_BUTTONS_PARAMS(COMMON_BUTTONS_PARAMS):
    ENROLL_SERVICES = "✍️ Enroll Service"
    RESERVATIONS = "✅ My Reservations"
    OUR_SERVICES = "✂️ Our Service"
    PRICES = "Prices"
    PAYMENTS = "Payments"
    ASK_ADMINISTRATOR = "❓ Ask Administrator"
    MAP = "🌐 Map"
    CONTACTS = "📍 Contacts"
    FAQ = "ℹ️ Frequent Questions"


@dataclass()
class MAIN_MANU_ADMIN_PARAMS(COMMON_BUTTONS_PARAMS):
    TIMETABLE = 'Timetable'
    SERVICES = "Service"
    CONTACTS = "CONTACTS"
    WORK_TIME = "Work time"
