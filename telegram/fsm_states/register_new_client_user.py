from aiogram.fsm.state import StatesGroup, State


class RegisterNewClientState(StatesGroup):
    new_client_name = State()  # for containing str
