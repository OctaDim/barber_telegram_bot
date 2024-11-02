import calendar


def get_month_dict_for_timetable(month: list, current_month: int):
    month_dict = {}

    for m in range(1, 13):
        if m in month:
            if m == current_month:
                month_dict[f'🔹{calendar.month_name[m]}'] = m
                continue

            month_dict[calendar.month_name[m]] = m
            continue

        month_dict[calendar.month_name[m]] = None

    return month_dict
