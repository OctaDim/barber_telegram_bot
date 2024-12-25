from aiogram.fsm.state import StatesGroup, State


class EnrollMethodsState(StatesGroup):
    selected_method_prefix = State()  # for containing str
