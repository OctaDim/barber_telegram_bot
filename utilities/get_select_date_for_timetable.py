from utilities.calendar_utils import get_month_name_by_number, get_weekday_flex_abbr_by_date


def get_select_date(date):
    select_month = get_month_name_by_number(month_number=date.month, language='RU')
    select_day = date.day
    weekday = get_weekday_flex_abbr_by_date(date_value=date, language='RU')

    data = {
        'weekday': f'{weekday}, {select_day}',
        'month': select_month
    }

    return data
