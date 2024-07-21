from aiogram.types import CallbackQuery, Message

from aiogram.fsm.context import FSMContext

from telegram.params.messages import CANNOT_USE_OBSOLETE_MSG
from telegram.telegram_utils.handlers_stack_utils import get_handler_answer_flag_dict


async def inline_keyboard_is_actual(state: FSMContext | dict,
                                    callback_query: CallbackQuery):

    async def message_inline_kbd_is_obsolete():
        await callback_query.answer(
            text=CANNOT_USE_OBSOLETE_MSG,
            show_alert=True)

    if isinstance(state, FSMContext):  # if state was passed as FSMContext obj
        state_data = await state.get_data()
    else:
        state_data = state  # if state argument was passed as dictionary

    ###### Check inline keyboard is obsolete because server was restarted
    if not state_data and "actual_message_min_id" not in state_data:
        await message_inline_kbd_is_obsolete()
        return False

    ###### Check inline keyboard is obsolete because new inl kbd was called
    minimal_actual_msg_id = state_data.get("actual_message_min_id")
    if callback_query.message.message_id < minimal_actual_msg_id:
        await message_inline_kbd_is_obsolete()
        return False

    return True


async def delete_inline_msg_and_next_msgs(
        callback_query: CallbackQuery,
        messages_number_to_delete: int) -> None:
    """Delete a specified number of the following messages starting
    from the inline keyboard message that triggered the callback query
    :param callback_query: CallbackQuery: The CallbackQuery object of
    the handled inline keyboard callback query message
    :param messages_number_to_delete: int: The number of messages to
    delete, including the inline keyboard message that triggered the
    callback query
    :return: None:
    """
    chat_id = callback_query.message.chat.id
    callback_query_message_id = callback_query.message.message_id

    for id_step in range(messages_number_to_delete):
        message_id_to_delete = callback_query_message_id + id_step

        await callback_query.bot.delete_message(chat_id=chat_id,
                                                message_id=message_id_to_delete)


async def delete_reply_msg_and_prev_msgs(message: Message,
                                         messages_number_to_delete: int) -> None:
    """Delete a specified number of the previous messages starting
    from the reply keyboard message that triggered the message.
    :param message: Message: The Message object of the handled reply
     keyboard message
    :param messages_number_to_delete: int: The number of messages to
    delete, including the reply keyboard message that triggered the
    message
    :return: None:
    """
    chat_id = message.chat.id
    message_id = message.message_id

    for id_step in range(messages_number_to_delete):
        message_id_to_delete = message_id - id_step

        await message.bot.delete_message(chat_id=chat_id,
                                         message_id=message_id_to_delete)
