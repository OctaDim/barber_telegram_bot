from dataclasses import dataclass

from telegram.params.buttons_common import COMMON_BUTTONS_PARAMS


@dataclass
class MAIN_MENU_BUTTONS(COMMON_BUTTONS_PARAMS):
    SERVICES = "💈 Услуги"
    BALANCE = "💰 Баланс"
    CONTACTS = "📍 Контакты"
    ASK_QUESTION = "❓ Задать Вопрос"


@dataclass()
class MAIN_MANU_ADMIN_PARAMS(COMMON_BUTTONS_PARAMS):
    TIMETABLE = 'Записи на услуги'
    SERVICES = "Услуги"
    CONTACTS = "Контакты"
    WORK_TIME = "Рабочий график"
