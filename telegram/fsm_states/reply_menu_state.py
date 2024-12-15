from aiogram.fsm.state import StatesGroup, State


class ReplyMenuState(StatesGroup):
    reply_keyboard_opened_state = State()  # for containing bool
    prior_reply_message_id_state = State()  # for containing int
