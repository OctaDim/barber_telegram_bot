import calendar


def get_month_dict(month):
    month_dict = {}

    for m in range(1, 13):
        if month > m:
            month_dict[calendar.month_name[m]] = None
            continue

        month_dict[calendar.month_name[m]] = True

    return month_dict
