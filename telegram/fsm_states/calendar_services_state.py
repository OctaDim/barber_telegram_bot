from aiogram.fsm.state import StatesGroup, State


class CalendarServicesState(StatesGroup):
    cur_month_enroll_srcs_calendar = State()  # for containing int
    cur_year_enroll_srcs_calendar = State()  # for containing int
    selected_date_enroll_srcs_calendar = State()  #  for containing date type
