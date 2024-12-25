from aiogram.fsm.state import StatesGroup, State


class EnrollMastersState(StatesGroup):
    selected_master_id = State()  # for containing int
    current_page_number_of_masters = State()  # for containing int
    paginated_masters_records = State()  # for containing dict[list]
