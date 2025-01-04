from dataclasses import dataclass

from telegram.params.buttons_common import COMMON_BUTTONS_PARAMS


@dataclass
class MAIN_MENU_BUTTONS(COMMON_BUTTONS_PARAMS):
    SERVICES = "💈 Services"
    BALANCE = "💰 Balance"
    CONTACTS = "📍 Contacts"
    ASK_QUESTION = "❓ Ask Question"


@dataclass()
class MAIN_MANU_ADMIN_PARAMS(COMMON_BUTTONS_PARAMS):
    TIMETABLE = 'Timetable'
    SERVICES = "Service"
    CONTACTS = "Contacts"
    WORK_TIME = "Work time"
