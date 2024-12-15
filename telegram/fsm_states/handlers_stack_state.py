from aiogram.fsm.state import StatesGroup, State


class HandlersReturnStackState(StatesGroup):
    handlers_stack = State()  # for containing list[dict]
