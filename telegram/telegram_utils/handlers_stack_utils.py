from aiogram.fsm.context import FSMContext

from telegram.telegram_utils.list_utils import empty_list_if_none


async def get_handlers_stack_list(state: FSMContext | dict) -> list:
    if isinstance(state, FSMContext):
        state_data = await state.get_data()
    else:
        state_data = state
    handlers_list = state_data.get("handlers_stack")
    handlers_list = empty_list_if_none(original_list=handlers_list)
    return handlers_list


async def execute_last_stack_handler(handlers_list: list[dict]) -> None:
    if len(handlers_list):
        return_hdr_function = handlers_list[-1].get("handler")
        return_hdr_event = handlers_list[-1].get("event")
        return_hdr_data = handlers_list[-1].get("data")

        await return_hdr_function(return_hdr_event, return_hdr_data)


def get_handler_answer_flag_dict(skip_handler_stack: bool = False,
                                 add_handler_stack: bool = False) -> dict:
    """
    Use this simple function to easily create dictionary with flag keys, which
    will be returned to the all update middleware from the handler.
    Result of this function may be returned from the handler optionally,
    but not necessarily. In the future flag keys can be added.

    :param skip_handler_stack: bool. Optional. True, if it is not necessary to
    add handler to the return handler stack.

    :param add_handler_stack: bool. Optional. True, if it is necessary to
    add handler with callback query (inline keyboard) to the return handler stack.
    Note: By default, all handlers from inline keyboards with callback will be skipped.

    :return: dictionary with keys as flags for the all update middleware
    """
    return locals()
