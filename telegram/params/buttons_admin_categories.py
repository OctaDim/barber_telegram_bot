from dataclasses import dataclass


@dataclass
class CHOOSE_SERVICE_OR_CATEGORIES:
    SERVICE = 'Услуги'
    CATEGORIES = 'Категории'


@dataclass
class ADMIN_CATEGORIES_ACTION:
    ADD = 'Добавить категорию'
    CHANGE = 'Изменить категорию'
    REMOVE = 'Удалить категорию'
