def get_time_duration_for_admin_preview(hours, minutes):
    if hours and minutes:
        return f'{hours}ч {minutes}м'

    elif hours == 0 and minutes:
        return f'{minutes}м'

    else:
        return f'{hours}ч'
