from datetime import timedelta

from aiogram.fsm.context import FSMContext


async def get_selected_services_ids(state: FSMContext | dict) -> list:
    if isinstance(state, FSMContext):  # if state was passed as FSMContext obj
        state_data = await state.get_data()
    else:
        state_data = state  # if state argument was passed as dictionary

    services_ids = state_data.get("selected_services_ids_state")
    services_ids = services_ids if services_ids is not None else []
    return services_ids


async def get_selected_services_cost(state: FSMContext | dict) -> float:
    if isinstance(state, FSMContext):  # if state was passed as FSMContext obj
        state_data = await state.get_data()
    else:
        state_data = state  # if state argument was passed as dictionary

    cost = state_data.get("selected_services_cost_state")
    cost = cost if cost is not None else float()
    return cost


async def get_services_duration(state: FSMContext | dict) -> timedelta:
    if isinstance(state, FSMContext):  # if state was passed as FSMContext obj
        state_data = await state.get_data()
    else:
        state_data = state  # if state argument was passed as dictionary

    duration = state_data.get("selected_services_duration_state")
    duration = duration if duration is not None else timedelta(0)
    return duration


async def clear_all_enroll_services_fsm_states(state: FSMContext):
    await state.update_data(
        all_services_info_state=None,
        selected_services_ids_state=None,
        selected_services_cost_state=None,
        selected_services_duration_state=None,
        cur_month_enroll_srcs_calendar=None,
        cur_year_enroll_srcs_calendar=None,
        selected_date_enroll_srcs_calendar=None)
