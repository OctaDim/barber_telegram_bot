from dataclasses import dataclass


@dataclass
class AddTimeDurationServiceMessage:
    SELECT_DURATION = 'Выберите продолжительность в <b>IN_HOURS</b> и <b>IN_MINUTES:</b>'
    HOURS = 'Часов:'
    MINUTES = 'Минут:'
    IN_HOURS = "часах"
    IN_MINUTES = "минутах"


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
