from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup


class ReplyMenuState(StatesGroup):
    reply_keyboard_opened_state = State()  # for containing bool
    prior_reply_message_id_state = State()  # for containing int
    prior_reply_kbd_markup_obj_state = State()  # for containing markup object
    prior_reply_kbd_text_state = State()  # for containing str
    prior_reply_kbd_img_path_state = State()  # for containing str
    prior_reply_kbd_img_text_state = State()  # for containing str
