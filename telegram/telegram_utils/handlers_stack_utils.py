import inspect

from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext


async def execute_last_stack_handler(handlers_list: list[dict]) -> None:
    if len(handlers_list):
        handler_callable_function_obj = handlers_list[-1].get("handler")
        handler_event = handlers_list[-1].get("event")
        handler_data = handlers_list[-1].get("data")

        print(f"{'-' * 115}\n\tFunction: {inspect.currentframe().f_code.co_name}\n")

        try:
            await handler_callable_function_obj(handler_event, handler_data)
            print(f"Last handler was executed successfully\n")
        except (TelegramBadRequest, Exception) as exception_info:
            print(f"Last handler was not executed: {exception_info}\n")


def get_handler_answer_flag_dict(
        add_handler_to_return_stack: bool = False,
        handler_messages_ids: list[int] = None,
        update_min_actual_msg_id: bool = False,
        executed_handler_name: str = None,
) -> dict:
    """
    Simple function to easily create dictionary with flag keys.
    Result of this function may be returned from the handler
    to the all update outer middleware optionally, but not necessarily.
    In the future flag keys can be added, if needed.

    :param add_handler_to_return_stack: bool. Optional.
    Define True to add handler to the handlers return stack to have
    possibility to return to this handler or directly execute this handler

    :param handler_messages_ids: list[int]. All messages ids of
    the current handler, that will be deleted on return button.
    Should be defined if add_handler_to_return_stack parameter is True

    :param update_min_actual_msg_id: bool. Optional.
    Define True to update actual message minimum id to check
    further if the message is obsolete.

    :param executed_handler_name: str: Name of the executed handler
    returned to middleware for logging aims

    :return: dictionary with flag keys and values, which can be read
    in middleware
    """
    return locals()  # Passing to return all named arguments


async def show_handlers_stack_logs(
        state: FSMContext,
        text: str = "Handlers stack logs (each handler messages ids):"
) -> None:
    state_data = await state.get_data()
    handlers_list = state_data.get("handlers_stack")
    print(f"\t{text}")
    if not handlers_list:
        print(f"\t\thandlers_list = []\n"
              f"\t\thandler_messages_ids = []\n")
    else:
        for idx in range(len(handlers_list)):
            handler_msgs_ids = handlers_list[idx].get("handler_messages_ids")
            handler_name = handlers_list[idx].get("handler_name")
            print(f"\t\t{idx}) {handler_msgs_ids} - {handler_name}")
        print()
