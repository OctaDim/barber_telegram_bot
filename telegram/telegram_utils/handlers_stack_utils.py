from aiogram.fsm.context import FSMContext


async def execute_last_stack_handler(handlers_list: list[dict]) -> None:
    if len(handlers_list):
        return_hdr_function = handlers_list[-1].get("handler")
        return_hdr_event = handlers_list[-1].get("event")
        return_hdr_data = handlers_list[-1].get("data")
        await return_hdr_function(return_hdr_event, return_hdr_data)


def get_handler_answer_flag_dict(skip_add_handler_stack: bool = False,
                                 upd_actual_msg_min_id: bool = False) -> dict:
    """
    Simple function to easily create dictionary with flag keys.
    Result of this function may be returned from the handler
    to the all update outer middleware optionally, but not necessarily.
    In the future flag keys can be added, if needed.

    :param skip_add_handler_stack: bool. Optional.
    Define True to skip adding handler to the handlers stack, otherwise
    any handler will be added to the handler stack automatically

    :param upd_actual_msg_min_id: bool. Optional.
    By default, any message id except inline message will update actual
    message minimum id. Define True to update actual message minimum id
    for inline message too.

    :return: dictionary with flag keys and values, which can be read
    in middleware
    """
    return locals()


async def clear_handlers_return_stack_fsm_state(state: FSMContext):
    await state.update_data(handlers_stack=None)
