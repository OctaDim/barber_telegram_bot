from aiogram.fsm.state import StatesGroup, State


class YesNoDialogState(StatesGroup):
    yes_no_dialog_msg_id_state = State()  # for containing int
