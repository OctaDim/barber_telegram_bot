from aiogram.fsm.state import StatesGroup, State


class ActualMessageIdState(StatesGroup):
    actual_message_min_id = State()  # for containing int
