from dataclasses import dataclass


@dataclass
class BUTTON_SERVICES_ACTION:
    ADD: str = 'Добавить услуги'
    CHANGE: str = 'Изменить услуги'
    Remove: str = 'Удалить услуги'
