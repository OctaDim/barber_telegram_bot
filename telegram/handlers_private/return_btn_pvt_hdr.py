from aiogram import Router, F
from aiogram.types import Message

from aiogram.fsm.context import FSMContext

from telegram.filters.chat_types_filter import ChatTypesFilter
from telegram.telegram_utils.delete_messages import delete_reply_msg_and_prev_msgs

from telegram.params.buttons_common import COMMON_BUTTONS_PARAMS
from telegram.params.messages import CAN_USE_LEFT_MENU

return_button_router = Router(name=__name__)
return_button_router.message.filter(ChatTypesFilter(["private"]))


@return_button_router.message(F.text == COMMON_BUTTONS_PARAMS.RETURN)
async def return_button_handler(message: Message,
                                state: FSMContext,
                                current_handler_data: dict):

    state_data = await state.get_data()
    handlers_list = state_data.get("handlers_stack")

    triggered_handler_data = {}

    if len(handlers_list) < 2:
        await message.answer(text=CAN_USE_LEFT_MENU)
        await state.update_data(handlers_stack=None)
        handlers_list = []

        print("\tTEST INFO: Return handler. Handlers stack cleared")
        print("\tTEST INFO: len(handlers_list): ", len(handlers_list))
        print()
        return

    elif len(handlers_list) == 2:
        await message.answer(text=CAN_USE_LEFT_MENU)
        await state.update_data(handlers_stack = None)
        handlers_list = []

        print("\tTEST INFO: Return handler. Handlers stack cleared")
        print("\tTEST INFO: len(handlers_list): ", len(handlers_list))
        print()
        return

    elif len(handlers_list) >= 3:
        triggered_handler_data = handlers_list[-3]

    triggered_hdr_function = triggered_handler_data.get("handler")
    triggered_hdr_event = triggered_handler_data.get("event")
    triggered_hdr_data = triggered_handler_data.get("data")

    # current_hdr_function = current_handler_data.get("handler")
    # current_hdr_event = current_handler_data.get("event")
    # current_hdr_data = current_handler_data.get("data")
    #
    # print(f"\t{triggered_hdr_function}")
    # print(f"\t{current_hdr_function}\n")
    #
    # print(f"\t{triggered_hdr_event}")
    # print(f"\t{current_hdr_event}\n")
    #
    # print(f"\t{triggered_hdr_data}")
    # print(f"\t{current_hdr_data}\n")


    # messages_number_to_delete =
    # await delete_reply_msg_and_prev_msgs(message=message,
    #                                      messages_number_to_delete=5)

    await triggered_hdr_function(triggered_hdr_event, triggered_hdr_data)

    del handlers_list[-2:]
    print("\tTEST INFO: Return handler. Handlers stack reduced by 2 records")
    print("\tTEST INFO: len(handlers_list): ", len(handlers_list))
    print()

    await state.update_data(handlers_stack=handlers_list)
