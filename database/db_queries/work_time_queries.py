import calendar
import time
from datetime import datetime

from database.db_engine_url import db_engine_url
from database.db_connection import DBConnection
from sqlalchemy import extract, func

from database.db_models.work_time_model import WorkTime

manager = DBConnection(db_url=db_engine_url)


def create_work_time(data: dict):
    with manager as session:
        start_time = data.get('time_start')
        end_time = data.get('time_end')
        delta = data.get('interval')
        year = data.get('year')
        month = data.get('month')
        days: list = data.get('days')

        for day in days:
            base_date = datetime.strptime(f"{year}-{month}-{day}", "%Y-%B-%d")

            session.add(WorkTime(
                start_time=base_date + start_time,
                end_time=base_date + end_time,
                delta=delta
            ))
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
            extract('year', WorkTime.start_time) == year
        ).group_by(
            extract('month', WorkTime.start_time)
        ).subquery()

        work_months = session.query(WorkTime).join(
            subquery, WorkTime.id == subquery.c.id
        ).all()

        data = []

        for month in work_months:
            data.append(month.start_time.month)

        return data


get_working_time_month_by_month_by_year(2024)


def get_one_day(id_day):
    with manager as session:
        day = session.query(WorkTime).filter(WorkTime.id == id_day).one()

        return day
