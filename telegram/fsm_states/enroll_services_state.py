from aiogram.fsm.state import StatesGroup, State


class EnrolledServicesState(StatesGroup):
    all_services_info_state: dict = State()
    selected_services_ids_state: list = State()
    selected_services_cost_state: float = State()
    selected_services_duration_state: float = State()
