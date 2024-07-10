from aiogram.fsm.state import StatesGroup, State


class LastNotInlineMessageIdState(StatesGroup):
    last_not_inline_msg_id_state = State()  # for containing int
