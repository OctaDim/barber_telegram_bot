from datetime import datetime

from sqlalchemy import extract, func, cast, Row, Integer, case

from database.db_connection import DBConnection
from database.db_engine_url import db_engine_url
from database.db_models.work_time_model import WorkTime
from telegram.config.logging import LOGGING
from utilities.decorators_global import execution_time_decorator


@execution_time_decorator(in_seconds=True,
                          note="All slots_records from now for month",
                          exec_time_logging=LOGGING.EXECUTION_TIME)
def get_slots_from_now_for_month(year: int, month: int,
                                 master_id: int = None) -> list[Row]:
    with (DBConnection(db_url=db_engine_url) as session):
        slot_records_for_month = session.query(
            cast(extract(
                "DAY", WorkTime.time_start), Integer).label("day_of_month"),
            WorkTime.master_id.label("master_id"),
            WorkTime.time_start.label("time_start"),
            WorkTime.time_end,
            WorkTime.active,
            WorkTime.reserved,
            (WorkTime.time_end - WorkTime.time_start).label("slot_duration"),
            func.lag(WorkTime.time_end).over(
                partition_by=extract("DAY", WorkTime.time_start),
                order_by=WorkTime.time_start).label("prior_slot_time_end"),
            case(
                (WorkTime.time_start == func.lag(WorkTime.time_end).over(
                    order_by=WorkTime.time_start), True),
                else_=False).label("continuing"),
        ).filter(
            WorkTime.time_start > datetime.now(),
            extract("YEAR", WorkTime.time_start) == year,
            extract("MONTH", WorkTime.time_start) == month,
            WorkTime.active.is_(True),
            WorkTime.reserved.is_(False),
            WorkTime.master_id == master_id
        ).order_by(
            "day_of_month",
            "time_start",
            "master_id"
        ).all()

        return slot_records_for_month

# ##################### TEST CODE ######################################
# ######################################################################
# year = 2024
# month = 10
# all_slots_records_by_month = get_slots_from_now_for_month(
#     year=year, month=month,
#     master_id=None)
# for record in all_slots_records_by_month:
#     print(f"{record.day_of_month}\t\t"
#           f"{record.master_id}\t\t"
#           f"{record.active}\t\t"
#           f"{record.reserved}\t\t"
#           f"{record.time_start}\t\t"
#           f"{record.time_end}\t\t"
#           f"{record.slot_duration}\t\t"
#           f"{record.continuing}\t\t"
#           f"{record.prior_slot_time_end}\t\t")
# ######################################################################
# ##################### END TEST CODE ##################################


# ################# TEMPORARY BACKUP OLD QUERIES #######################
# ######################################################################
# @execution_time_decorator(in_seconds=True, note="Enrollment days (no subquery)",
#                           exec_time_logging=LOGGING.EXECUTION_TIME)
# def get_enrollment_days(year: int, month: int,
#                         duration: timedelta) -> list[int]:
#     with DBConnection(db_url=db_engine_url) as session:
#         records = session.query(
#             extract("day_of_month", WorkTime.time_start).label("day_of_month")).filter(
#             extract("year", WorkTime.time_start) == year,
#             extract("month", WorkTime.time_start) == month,
#             WorkTime.time_end - WorkTime.time_start >= duration).order_by(
#             "day_of_month").distinct("day_of_month").all()
#
#         enrolment_days_list = [int(record.day) for record in records]
#         return enrolment_days_list
#
#
# @execution_time_decorator(in_seconds=True, note="Enrollment days (with subquery)",
#                           exec_time_logging=LOGGING.EXECUTION_TIME)
# def get_enrollment_days_sub_qry(year: int, month: int,
#                                 duration: timedelta) -> list[int]:
#     with DBConnection(db_url=db_engine_url) as session:
#         subquery = session.query(WorkTime.id).filter(
#             extract("year", WorkTime.time_start) == year).subquery()
#
#         records = session.query(
#             extract("day_of_month", WorkTime.time_start).label("day_of_month")).join(
#             subquery, WorkTime.id == subquery.c.id).filter(
#             extract("month", WorkTime.time_start) == month,
#             WorkTime.time_end - WorkTime.time_start >= duration).order_by(
#             "day_of_month").distinct("day_of_month").all()
#         return records
#
#
# @execution_time_decorator(in_seconds=True, note="Enrollment days (with sub-subquery)",
#                           exec_time_logging=LOGGING.EXECUTION_TIME)
# def get_enrollment_days_sub_sub_qry(year: int, month: int,
#                                     duration: timedelta) -> list[int]:
#     with DBConnection(db_url=db_engine_url) as session:
#         sub_subquery = session.query(WorkTime.id).filter(
#             extract("year", WorkTime.time_start) == year).subquery()
#
#         subquery = session.query(WorkTime.id).join(
#             sub_subquery, WorkTime.id == sub_subquery.c.id).filter(
#             extract("month", WorkTime.time_start) == month).subquery()
#
#         records = session.query(
#             extract("day_of_month", WorkTime.time_start).label("day_of_month")).join(
#             subquery, WorkTime.id == subquery.c.id).filter(
#             WorkTime.time_end - WorkTime.time_start >= duration).order_by(
#             "day_of_month").distinct("day_of_month").all()
#         return records
