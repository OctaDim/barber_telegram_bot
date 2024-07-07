async def execute_last_handler(handlers_list: list[dict]) -> None:
    return_hdr_function = handlers_list[-1].get("handler")
    return_hdr_event = handlers_list[-1].get("event")
    return_hdr_data = handlers_list[-1].get("data")

    await return_hdr_function(return_hdr_event, return_hdr_data)
