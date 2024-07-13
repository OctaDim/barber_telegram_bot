from aiogram.filters.callback_data import CallbackData


class NoActionCommonCBData(CallbackData, prefix="no_action_inl_common"):
    pass


class ReturnInlineBtnCBData(CallbackData, prefix="return_inl_common"):
    pass


class MainMenuInlineBtnCBData(CallbackData, prefix="main_menu_inl_common"):
    pass
