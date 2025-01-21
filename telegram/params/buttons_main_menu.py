from dataclasses import dataclass

from telegram.config.admin_configs import ADMIN_CATEGORIES_CONFIGS
from telegram.params.buttons_common import COMMON_BUTTONS_PARAMS


@dataclass
class MAIN_MENU_BUTTONS(COMMON_BUTTONS_PARAMS):
    SERVICES = "💈 Услуги"
    BALANCE = "💰 Баланс"
    CONTACTS = "📍 Контакты"
    ASK_QUESTION = "❓ Задать Вопрос"


@dataclass()
class MAIN_MANU_ADMIN_PARAMS(COMMON_BUTTONS_PARAMS):
    TIMETABLE = 'Управление Расписанием'
    CONTACTS = "Контакты"
    WORK_TIME = "Создание \nГрафика"
    SERVICES = 'Услуги'
    CATEGORIES = 'Услуги и Категории'
    SERVICES = CATEGORIES if ADMIN_CATEGORIES_CONFIGS.USE_CATEGORY \
        else SERVICES
