from aiogram.types import InlineKeyboardMarkup


def tick_the_button(target_text, keyboard):
    new_text = '✅' + target_text

    for row in keyboard:
        for button in row:
            if target_text[-1] in button.text:
                if target_text == button.text:
                    button.text = new_text

                else:
                    button.text = button.text.replace('✅', '')

    new_keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)

    return new_keyboard
