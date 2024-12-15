from aiogram.fsm.state import StatesGroup, State


class ReservationsClientState(StatesGroup):
    current_page_number_of_reservations = State()  # for containing int
    paginated_reservations_records = State()  # for containing dict[list]
    reservation_message_id_state = State()  # for containing int
