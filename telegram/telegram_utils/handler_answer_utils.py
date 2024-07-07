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
