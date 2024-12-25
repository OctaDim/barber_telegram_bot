import inspect
from typing import Union, Literal

from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_yes_no_dialog_inline_message_kbd_pvt(
        yes_answer_callback_data_obj_no_pack: CallbackData,
        no_answer_callback_data_obj_no_pack: CallbackData,
        yes_button_text: str,
        no_button_text: str
) -> InlineKeyboardMarkup:
    builder_inl_kbd = InlineKeyboardBuilder()

    builder_inl_kbd.button(
        text=yes_button_text,
        callback_data=yes_answer_callback_data_obj_no_pack.pack())

    builder_inl_kbd.button(
        text=no_button_text,
        callback_data=no_answer_callback_data_obj_no_pack.pack())

    builder_inl_kbd.adjust(2)

    inline_kbd_markup = builder_inl_kbd.as_markup()
    return inline_kbd_markup


async def open_yes_no_dialog_and_get_answer(
        initial_trigger_callback_data_cls: type[CallbackData],
        yes_no_answer_callback_data_cls: type[CallbackData],
        callback_query: CallbackQuery,
        callback_data: CallbackData,
        state: FSMContext,
        yes_no_dialog_msg_text: Union[
            Literal["any answer", "any confirmation"], str] = "Confirm action?",
        yes_button_text: str = "YES",
        no_button_text: str = "NO"
) -> Union[None, Literal["yes", "no"]]:
    """Open yes-no dialog with answer, confirmation or any other dialog text.
    The returned result of the function may be used to execute the following logic.
    This function should be placed in an initial handler, where basic logic
    will be executed after receiving "yes" or "no" return (means yes or no answer).

    :param initial_trigger_callback_data_cls: type[CallbackData]: (Class, NOT object!!!)
    Initial CallbackData Class, that triggers handler executing where logic
    depends on the yes or no answer.

    :param yes_no_answer_callback_data_cls: type[CallbackData]: (Class, NOT object!!!)
    IMPORTANT!!!: This Class must contain binding attribute <yes_no_dialog_answer: str>
    CallbackData Class, that will be returned from the yes-no dialog.
    This CallbackData must be added to the router decorator of the same handler as above

    :param callback_query: CallbackQuery: Standard inline keyboard handler parameter
    :param callback_data: CallbackData: Standard inline keyboard handler parameter
    :param state: FSMContext: Standard inline keyboard handler parameter

    :param yes_no_dialog_msg_text: str: Any custom answer, confirmation or text
    :param yes_button_text: str: Any custom button caption text, that returns True
    :param no_button_text:: str: Any custom button caption text, that returns False
    :return: Union[None, Literal["yes", "no"]]
    None - if yes-no dialog just opened and not received answer yet
    "yes" or "no" - result, if yes-no button clicked and answer received
    """

    print(f"{'-' * 115}\n\tFunction: {inspect.currentframe().f_code.co_name}\n")

    callback_prefix = callback_data.__prefix__

    if callback_prefix == initial_trigger_callback_data_cls.__prefix__:
        print(f"\tTrigger Initial callback_data logic execution:\n"
              f"\tcallback_data Class = {initial_trigger_callback_data_cls.__name__}\n")

        await callback_query.answer()

        trigger_callback_data_attrs = callback_data.__dict__
        print(f"\tTrigger cb data obj attributes copied to answer cb data object:\n"
              f"\tcallback_data.__dict__ = {callback_data.__dict__}")
        for attr_name, attr_value in trigger_callback_data_attrs.items():
            setattr(yes_no_answer_callback_data_cls, attr_name, attr_value)
            print(f"\t\t\tCopied attribute: {attr_name} = {attr_value}")

        yes_callback_data_obj = yes_no_answer_callback_data_cls(
            yes_no_dialog_answer="yes")
        no_callback_data_obj = yes_no_answer_callback_data_cls(
            yes_no_dialog_answer="no")
        print(f"\n\tNew yes-no callback_data objects created:\n"
              f"\tyes_callback_data_obj.yes_no_dialog_answer = "
              f"\t{yes_callback_data_obj.yes_no_dialog_answer}\n"
              f"\tno_callback_data_obj.yes_no_dialog_answer = "
              f"\t{no_callback_data_obj.yes_no_dialog_answer}\n")

        yes_no_message = await callback_query.message.answer(
            text=yes_no_dialog_msg_text,
            reply_markup=get_yes_no_dialog_inline_message_kbd_pvt(
                yes_answer_callback_data_obj_no_pack=yes_callback_data_obj,
                no_answer_callback_data_obj_no_pack=no_callback_data_obj,
                yes_button_text=yes_button_text,
                no_button_text=no_button_text))
        yes_no_message_id = yes_no_message.message_id
        print(f"\tDialog yes-no inline keyboard message created:\n"
              f"\tyes_no_message_id (created) = {yes_no_message_id}\n")

        await state.update_data(
            yes_no_dialog_msg_id_state=yes_no_message_id)
        print(f"\tFSM State updated:\n"
              f"\tyes_no_dialog_msg_id_state = {yes_no_message_id}\n")

    elif callback_prefix == yes_no_answer_callback_data_cls.__prefix__:
        print(f"\tAnswer yes-no callback_data logic execution:\n"
              f"\tcallback_data Class = {yes_no_answer_callback_data_cls.__name__}\n")

        await callback_query.answer()

        bot = callback_query.bot
        state_data = await state.get_data()
        yes_no_message_id = state_data.get("yes_no_dialog_msg_id_state")
        await bot.delete_message(message_id=yes_no_message_id,
                                 chat_id=callback_query.message.chat.id)
        print(f"\tDialog yes-no inline keyboard message deleted\n"
              f"\tyes_no_message_id (deleted) = {yes_no_message_id}\n")

        yes_no_dialog_answer = callback_data.yes_no_dialog_answer
        print(f"\tFunction result returned:\n"
              f"\tyes_no_dialog_answer = {yes_no_dialog_answer}\n")

        return yes_no_dialog_answer
