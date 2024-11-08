from aiogram.fsm.state import StatesGroup, State


class IntervalSlotsState(StatesGroup):
    selected_interval_first_slot_id = State()  # for containing int
    enrollment_intervals_state = State()  # for containing dict[dict]
    current_page_number_of_intervals = State()  # for containing int
    paginated_intervals_dicts_list = State()  # for containing dict[list]
