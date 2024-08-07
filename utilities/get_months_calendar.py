import calendar


def month_list(date):
    month = date.month

    month_dict = []

    for m in range(month, 13):
        month_dict.append(calendar.month_name[m])

    return month_dict
