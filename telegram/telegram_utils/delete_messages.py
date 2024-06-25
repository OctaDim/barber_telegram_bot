from aiogram import Bot
from aiogram.types import CallbackQuery, Message


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
