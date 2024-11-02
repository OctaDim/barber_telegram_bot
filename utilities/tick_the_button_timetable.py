from aiogram.types import InlineKeyboardMarkup


def tick_the_button_timetable(target_text, keyboard, current_day):
    new_text = '✅' + target_text

    for row in keyboard:
        for button in row:
            if target_text in button.text:
                if target_text == button.text or '🔹' in button.text:
                    button.text = new_text
                    continue
            else:
                button.text = button.text.replace('✅', '')

            if current_day:
                if str(current_day) == button.text:
                    button.text = '🔹' + button.text

    new_keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)

    return new_keyboard
