from dataclasses import dataclass


@dataclass
class AddTimeDurationServiceMessage:
    SELECT_DURATION = 'Выберите продолжительность в <b>часах</b> и <b>минутах</b>:'
    HOURS = 'Часов:'
    MINUTES = 'Минут:'
    IN_HOURS = 'часах'
    IN_MINUTES = 'минутах'


@dataclass
class AddPriceMessage:
    ENTER_NUMBER = 'Введите число'


@dataclass
class GetDecision:
    ADD = 'Услуга добавлена'
    REMOVE = 'Услуга удалена'
    CHANGE = 'Выберите для изменения'


@dataclass
class ChangeService:
    NAME = 'Введите новое название услуги'
    DESCRIPTION = 'Введите новое описание для услуги'
    PRICE = 'Введите новую цену для услуги'


service_details_message = (
    'Название: {}\n'
    'Описание: {}\n'
    'Продолжительность: {}\n'
    'Цена: {}\n'
)

ADD_CATEGORY = 'Выберите категорию в которую хотите добавить созданную услугу'
