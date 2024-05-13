from dataclasses import dataclass
from telegram.params.buttons_common import COMMON_BUTTONS_PARAMS



@dataclass
class MAIN_MENU_BUTTONS_PARAMS(COMMON_BUTTONS_PARAMS):
    FREE_TIME = "Free Time"
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
    ADD_SERVICES = "Add services"
    CHANGE_SERVICES = "Change services"
    ADD_CONTACTS = "Add contacts"
    CHANGE_CONTACTS = "Change contacts"
