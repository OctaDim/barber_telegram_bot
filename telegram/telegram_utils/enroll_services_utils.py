from datetime import timedelta

from aiogram.fsm.context import FSMContext

from telegram.telegram_utils.list_utils import empty_list_if_none


async def get_selected_services_ids(state: FSMContext|dict) -> list:
    if isinstance(state, FSMContext):  # if state was passed as FSMContext obj
        state_data = await state.get_data()
    else:
        state_data = state  # if state argument was passed as dictionary

    selected_services_ids = state_data.get("selected_services_ids_state")
    selected_services_ids = empty_list_if_none(original_list=selected_services_ids)

    return selected_services_ids


async def get_selected_services_cost(state: FSMContext|dict) -> float:
    if isinstance(state, FSMContext):  # if state was passed as FSMContext obj
        state_data = await state.get_data()
    else:
        state_data = state  # if state argument was passed as dictionary

    selected_services_cost = state_data.get("selected_services_cost_state")
    if selected_services_cost is None:
        selected_services_cost = float()

    return selected_services_cost


async def get_selected_services_duration(state: FSMContext|dict) -> timedelta:
    if isinstance(state, FSMContext):  # if state was passed as FSMContext obj
        state_data = await state.get_data()
    else:
        state_data = state  # if state argument was passed as dictionary

    selected_services_duration = state_data.get("selected_services_duration_state")
    if selected_services_duration is None:
        selected_services_duration = timedelta(0)

    return selected_services_duration
