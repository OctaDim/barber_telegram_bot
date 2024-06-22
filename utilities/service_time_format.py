def get_time_duration_for_admin_preview(hours, minutes):
    if hours and minutes:
        return f'{hours}h {minutes}m'

    elif hours == 0 and minutes:
        return f'{minutes}m'

    else:
        return f'{hours}h'
