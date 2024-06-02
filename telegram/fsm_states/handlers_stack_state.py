from aiogram.fsm.state import StatesGroup, State


class HandlersReturnStackState(StatesGroup):
    handlers_stack: list = State()
