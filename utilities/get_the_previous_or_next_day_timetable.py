from database.db_queries.work_time_queries import get_working_time_month_by_month_by_year, get_work_time_by_month, \
    get_all_work_years


def get_previous_or_next_int(
        list_integers: list,
        select_integer: int,
        previous_integer: bool = False,
        next_integer: bool = False
):
    previous_integers = []
    next_integers = []

    for integer in list_integers:
        if integer == select_integer:
            continue

        if integer < select_integer:
            previous_integers.append(integer)
            continue

        next_integers.append(integer)

    if len(previous_integers) != 0:
        previous_integers = max(previous_integers)

    if len(next_integers) != 0:
        next_integers = min(next_integers)

    if previous_integer:
        return previous_integers

    if next_integer:
        return next_integers

    return previous_integers, next_integers


def get_other_month(select_year: int, select_month: int, action: bool, master_id: int) -> dict | None:
    """
        action: True - next, False - previous
    """
    other_months = get_working_time_month_by_month_by_year(year=select_year)

    previous_months, next_months = get_previous_or_next_int(list_integers=other_months, select_integer=select_month)

    if action:
        if next_months:
            days = get_work_time_by_month(month=next_months, year=select_year, list_checker=True, master_id=master_id)

            data = {
                'month': next_months,
                'year': select_year,
                'day': days[0]
            }

            return data

        years = get_all_work_years()

        next_year = get_previous_or_next_int(select_integer=select_year, list_integers=years, next_integer=True)

        if next_year:
            months = get_working_time_month_by_month_by_year(year=next_year)
            days = get_work_time_by_month(month=months[0], year=next_year, list_checker=True, master_id=master_id)

            data = {
                'month': months[0],
                'day': days[0],
                'year': next_year
            }

            return data

        return None

    if previous_months:
        if previous_months:
            days = get_work_time_by_month(month=previous_months, year=select_year, list_checker=True,
                                          master_id=master_id)

            data = {
                'month': previous_months,
                'year': select_year,
                'day': days[-1]
            }

            return data

        years = get_all_work_years()

        previous_year = get_previous_or_next_int(select_integer=select_year, list_integers=years, previous_integer=True)

        if previous_year:
            months = get_working_time_month_by_month_by_year(year=previous_year)
            days = get_work_time_by_month(month=months[-1], year=previous_year, list_checker=True, master_id=master_id)

            data = {
                'month': months[-1],
                'day': days[-1],
                'year': previous_year
            }

            return data

        return None
