from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from telegram.keyboard_inline.common_buttons_inline import (
    create_main_menu_inline_button)
from telegram.params.buttons_submenu_balance import (
    BALANCE_BUTTONS)


class BalanceClientInlineMenuCBData(CallbackData, prefix="balance client inl menu"):
    pass


class DepositBalanceInlineMenuCBData(CallbackData, prefix="deposit balance inl menu"):
    pass


class PaymentsHistoryInlineMenuCBData(CallbackData, prefix="payments history inl menu"):
    pass


def get_balance_inl_kbd_pvt() -> InlineKeyboardMarkup:
    builder_inl_kbd = InlineKeyboardBuilder()

    builder_inl_kbd.button(text=BALANCE_BUTTONS.MY_BALANCE,
                           callback_data=BalanceClientInlineMenuCBData())

    builder_inl_kbd.button(text=BALANCE_BUTTONS.DEPOSIT_BALANCE,
                           callback_data=DepositBalanceInlineMenuCBData())

    builder_inl_kbd.button(text=BALANCE_BUTTONS.PAYMENTS_HISTORY,
                           callback_data=PaymentsHistoryInlineMenuCBData())

    # builder_inl_kbd.add(create_return_inline_button(
    #     delete_inline_msg_on_return=True))
    builder_inl_kbd.add(create_main_menu_inline_button())
    # builder_inl_kbd.add(create_empty_no_action_inl_btn())

    # builder_inl_kbd.adjust(1, 1, 1, 2)
    builder_inl_kbd.adjust(1, 1, 1, 1)

    inline_kbd_markup = builder_inl_kbd.as_markup()
    return inline_kbd_markup
