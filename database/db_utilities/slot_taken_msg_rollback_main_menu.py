from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from telegram.handlers_private.main_menu_btn_pvt_hdr import return_main_menu_btn_handler
from telegram.params.messages import SLOT_ALREADY_TAKEN


async def slot_taken_msg_rollback_main_menu(message: Message,
                                            ongoing_session,
                                            state: FSMContext) -> None:
    await message.answer(text=SLOT_ALREADY_TAKEN)
    ongoing_session.rollback()

    # Call the same functionality handler of the reply keyboard button
    await return_main_menu_btn_handler(message=message, state=state)
