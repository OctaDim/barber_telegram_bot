import calendar
import time

from sqlalchemy.orm import joinedload

import database.db_initialization

from datetime import datetime, timedelta

from database.db_engine_url import db_engine_url
from database.db_connection import DBConnection
from sqlalchemy import extract, func

from database.db_models.break_time_model import BreakTime
from database.db_models.user_model import User
from database.db_models.work_time_model import WorkTime
from database.db_queries.get_master_obj_by_telegram_id import get_master_id_by_telegram_id
from database.db_utilities.model_object_update import update_object

manager = DBConnection(db_url=db_engine_url)


def create_work_time(
        time_start: datetime,
        time_end: datetime,
        slot_duration: timedelta,
        master_id: int
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


def get_work_time_by_month(month, year, master_id: int, list_checker=False):
    with manager as session:
        work_days = session.query(WorkTime).filter(
            extract('year', WorkTime.time_start) == year,
            WorkTime.master_id == master_id).group_by(WorkTime).having(
            extract('month', WorkTime.time_start) == month).all()
        data = {}

        for day in work_days:
            data[day.time_start.day] = day.time_start.date()

        if list_checker:
            data_list = []

            for key in data.keys():
                data_list.append(key)

            return data_list

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


def get_day_work_time(date_day: datetime.date):
    with manager as session:
        work_time = session.query(WorkTime).options(
            joinedload(WorkTime.work_time_clients),
            joinedload(WorkTime.work_time_masters),
        ).filter(
            extract('year', WorkTime.time_start) == date_day.year,
            extract('month', WorkTime.time_start) == date_day.month,
            extract('day', WorkTime.time_start) == date_day.day
        ).order_by(WorkTime.time_start).all()

        return work_time


def get_break_time_by_day(date_day: datetime.date):
    with manager as session:
        break_time = session.query(BreakTime).filter(
            extract('year', BreakTime.start_break) == date_day.year,
            extract('month', BreakTime.start_break) == date_day.month,
            extract('day', BreakTime.start_break) == date_day.day
        ).all()

        return break_time


def get_all_work_years():
    with manager as session:
        years = session.query(WorkTime).distinct(
            extract('year', WorkTime.time_start)
        ).all()

        data = []

        for i in years:
            data.append(i.time_start.year)

        return data


def get_one_slots(work_time_id: int):
    with manager as session:
        data = session.query(WorkTime).options(
            joinedload(WorkTime.work_time_clients),
            joinedload(WorkTime.work_time_services),
            joinedload(WorkTime.work_time_masters)
        ).filter(WorkTime.id == work_time_id).first()

        return data


def make_slot_inactive_or_active(work_time_id: int):
    with manager as session:
        db_object = session.query(WorkTime).filter(WorkTime.id == work_time_id).first()
        if db_object.active:
            data = {'active': False}
        else:
            data = {'active': True}

        update_object(
            obj=db_object,
            data=data,
            session=session
        )


def update_time_start_and_time_end(data: dict, work_time_obj: WorkTime):
    with manager as session:
        db_object = session.query(WorkTime).filter(WorkTime.id == work_time_obj.id).first()

        update_object(
            obj=db_object,
            data=data,
            session=session
        )

        return True


def create_work_time_by_break_time(break_id: int):
    with manager as session:
        obj_break_time = session.query(BreakTime).options(
            joinedload(BreakTime.break_time_masters)
        ).filter(BreakTime.id == break_id).first()

        update_object(
            data={'active': False},
            obj=obj_break_time,
            session=session
        )

        time_start = obj_break_time.start_break
        time_end = obj_break_time.end_break
        slot_duration = obj_break_time.end_break - obj_break_time.start_break
        master_id = obj_break_time.break_time_masters[0].id

        create_work_time(
            time_start=time_start,
            time_end=time_end,
            slot_duration=slot_duration,
            master_id=master_id
        )

        return time_start.date()
