from aiogram.fsm.state import StatesGroup, State


class EnrollServicesStates(StatesGroup):
    selected_action = State()
    selected_services_ids = State()
    selected_total_cost = State()
    selected_total_duration = State()
