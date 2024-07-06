from aiogram.fsm.state import StatesGroup, State


class EnrolledServicesState(StatesGroup):
    all_services_info_state = State()  # for containing dict[str, bool]
    last_enroll_services_msg_id = State()  # for containing int
    selected_services_ids_state = State()  # for containing list[int]
    selected_services_cost_state = State()  # for containing float
    selected_services_duration_state = State()  # for containing float
