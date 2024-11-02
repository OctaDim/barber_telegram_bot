from datetime import datetime


def get_cb_data_of_day_timetable(keyboard):
    for row in keyboard:
        for button in row:
            if '✅' in button.text:
                data: str = button.callback_data
                valid_format_data = data.split(':')

                date_day = datetime.fromisoformat(valid_format_data[-1]).date()

                return date_day
