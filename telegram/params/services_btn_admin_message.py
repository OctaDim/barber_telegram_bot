from dataclasses import dataclass


@dataclass
class AddTimeDurationServiceMessage:
    SELECT_DURATION = 'Select the duration of the service in <b>HOURS</b> and <b>MINUTES:</b>'
    HOURS = 'Hours:'
    MINUTES = 'Minutes:'


@dataclass
class AddPriceMessage:
    ENTER_NUMBER = 'Enter a number'


@dataclass
class GetDecision:
    ADD = 'Service added.'
    REMOVE = 'Service removed.'
    CHANGE = 'Choose what you want to change.'


@dataclass
class ChangeService:
    NAME = 'Enter a new name for the service'
    DESCRIPTION = 'Enter a new description for the service'
    PRICE = 'Enter a new price for the service'
