import calendar
import time
from datetime import datetime, timedelta

from database.db_engine_url import db_engine_url
from database.db_connection import DBConnection
from sqlalchemy import extract, func

from database.db_models.break_time_model import BreakTime
from database.db_models.work_time_model import WorkTime

manager = DBConnection(db_url=db_engine_url)


def create_work_time(
        time_start: datetime,
        time_end: datetime,
        slot_duration: timedelta,
):

    with manager as session:
        work_time = WorkTime(
            time_start=time_start,
            time_end=time_end,
            slot_duration=slot_duration
        )

        session.add(work_time)
        session.commit()



def create_break_time(
        start_break: datetime,
        end_break: datetime,
):
    with manager as session:
        break_time = BreakTime(
            start_break=start_break,
            end_break=end_break
        )

        session.add(break_time)
        session.commit()


def get_work_time_by_month(month, year):
    month_number = list(calendar.month_name).index(month.capitalize())

    with manager as session:
        work_days = session.query(WorkTime).filter(
            extract('year', WorkTime.start_time) == year).group_by(WorkTime).having(
            extract('month', WorkTime.start_time) == month_number).all()

        data = {}

        for day in work_days:
            data[day.start_time.day] = day.id

        return data


def get_working_time_month_by_month_by_year(year):
    with manager as session:
        subquery = session.query(
            func.min(WorkTime.id).label('id')
        ).filter(
            extract('year', WorkTime.time_start) == year
        ).group_by(
            extract('month', WorkTime.time_start)
        ).subquery()

        work_months = session.query(WorkTime).join(
            subquery, WorkTime.id == subquery.c.id
        ).all()

        data = []

        for month in work_months:
            data.append(month.time_start.month)

        return data


get_working_time_month_by_month_by_year(2024)


def get_one_day(id_day):
    with manager as session:
        day = session.query(WorkTime).filter(WorkTime.id == id_day).one()

        return day
