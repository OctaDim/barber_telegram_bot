from aiogram.fsm.context import FSMContext


async def clear_all_enroll_services_fsm_states(state: FSMContext):
    await state.update_data(
        all_services_info_state=None,
        selected_services_ids_state=None,
        selected_services_cost_state=None,
        selected_services_duration_state=None,
        cur_month_enroll_srcs_calendar=None,
        cur_year_enroll_srcs_calendar=None,
        selected_date_enroll_srcs_calendar=None)
