from aiogram.utils.keyboard import ReplyKeyboardBuilder, ReplyKeyboardMarkup

from telegram.params.button_admin_panel_or_main_menu import ButtonAdminPanelOrMainMenu


def return_admin_panel_or_main_menu_kbd(quantity: int = None ) -> ReplyKeyboardMarkup:
    builder_reply_kbd = ReplyKeyboardBuilder()

    builder_reply_kbd.button(text=ButtonAdminPanelOrMainMenu.MAIN_MANU)
    builder_reply_kbd.button(text=ButtonAdminPanelOrMainMenu.ADMIN_PANEL)

    builder_reply_kbd.adjust(1)

    reply_keyboard_markup = builder_reply_kbd.as_markup(
        resize_keyboard=True,
        one_time_keyboard=False)

    return reply_keyboard_markup
