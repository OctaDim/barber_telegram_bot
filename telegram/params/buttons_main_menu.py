from dataclasses import dataclass
from telegram.params.buttons_common import COMMON_BUTTONS_PARAMS



@dataclass
class MAIN_MENU_BUTTONS_PARAMS(COMMON_BUTTONS_PARAMS):
    ENROLL_SERVICES = "Enroll Services"
    RESERVATIONS = "My Reservations"
    SERVICES = "Services"
    PRICES = "Prices"
    PAYMENTS = "Payments"
    ASK_ADMINISTRATOR = "Ask Administrator"
    MAP = "Map"
    CONTACTS = "Contacts"
    FAQ = "Frequent Questions"


@dataclass()
class MAIN_MANU_ADMIN_PARAMS(COMMON_BUTTONS_PARAMS):
    SERVICES = "Services"
    CONTACTS = "CONTACTS"
