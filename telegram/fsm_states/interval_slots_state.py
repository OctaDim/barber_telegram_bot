from aiogram.fsm.state import StatesGroup, State


class IntervalSlotsState(StatesGroup):
    selected_interval_first_slot_id = State()  # for containing int
    enrollment_intervals_state = State()  # for containing dict
