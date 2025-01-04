from dataclasses import dataclass


@dataclass
class BUTTON_SERVICES_ACTION:
    ADD: str = 'Add services'
    CHANGE: str = 'Change services'
    Remove: str = 'Remove services'
