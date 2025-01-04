import re

from telegram.params.work_time_cb_data_message import HOUR_ABBREVIATION


def get_the_time_from_the_inl_keyboard(keyboard):
    data = ''

    for row in keyboard:
        for button in row:
            if '✅' in button.text:
                if HOUR_ABBREVIATION in button.text:
                    button_text = re.sub(r'\D+', '', button.callback_data)
                    data += str(button_text)
                    continue

                button_text = re.sub(r'\D+', '', button.callback_data)

                if len(button_text) == 1:
                    data += f':0{button_text}'
                    continue

                data += f':{button_text}'

    return data
