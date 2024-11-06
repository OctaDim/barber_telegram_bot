from datetime import datetime
from typing import Union, Optional, Tuple

from sqlalchemy import extract, func, cast, Integer, case

from database.db_connection import DBConnection
from database.db_engine_url import db_engine_url
from database.db_models.user_model import User
from database.db_models.work_time_model import WorkTime
from database.db_utilities.create_order_by_partial_query import (
    create_order_by_partial_query)
from telegram.config.logging import LOGGING
from utilities.decorators_global import execution_time_decorator


@execution_time_decorator(in_seconds=True,
                          note="All slots_records from now for month",
                          exec_time_logging=LOGGING.EXECUTION_TIME)
def get_slots_from_now_for_month(
        year: int,
        month: int,
        worktime_id: Union[int, "all"] = "all",
        master_id: Union[int, "all"] = "all",
        worktime_client_obj: Union[int, "all"] = "all",
        reserved: Union[bool, "all"] = "all",
        active: Union[bool, "all"] = "all",
        admin_only: Union[bool, "all"] = "all",
        order_by_fields: Optional[Union[str, Tuple[str, ...], None]] = (
                "day_of_month", "time_start",)
) -> list[WorkTime]:
    with DBConnection(db_url=db_engine_url) as session:
        base_query = session.query(
            WorkTime.id,
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
                else_=False).label("continuing"))

        filter_query = base_query.filter(
            WorkTime.time_start > datetime.now(),
            extract("YEAR", WorkTime.time_start) == year,
            extract("MONTH", WorkTime.time_start) == month)

        if worktime_id != "all":
            filter_query = filter_query.filter(
                WorkTime.id == worktime_id)

        if master_id != "all":
            filter_query = filter_query.filter(
                WorkTime.master_id == master_id)

        if worktime_client_obj != "all":
            filter_query = filter_query.filter(
                WorkTime.work_time_clients.any(User.id == worktime_client_obj))

        if reserved != "all":
            filter_query = filter_query.filter(
                WorkTime.reserved.is_(reserved))

        if active != "all":
            filter_query = filter_query.filter(
                WorkTime.active.is_(active))

        if admin_only != "all":
            filter_query = filter_query.filter(
                WorkTime.admin_only.is_(admin_only))

        order_query = create_order_by_partial_query(
            model_class=WorkTime,
            prior_filter_query=filter_query,
            order_by_fields=order_by_fields)

        slot_records_for_month = order_query.all()
        return slot_records_for_month

# ##################### TEST CODE ######################################
# ######################################################################
# year = 2024
# month = 10
# master_id = 1
# all_slots_records_by_month = get_slots_from_now_for_month(
#     year=year, month=month
# )
# for record in all_slots_records_by_month:
#     print(f"{record.id}\t\t"
#           f"{record.day_of_month}\t\t"
#           f"{record.master_id}\t\t"
#           f"{record.active}\t\t"
#           f"{record.reserved}\t\t"
#           f"{record.time_start}\t\t"
#           f"{record.time_end}\t\t"
#           f"{record.slot_duration}\t\t"
#           f"{record.continuing}\t\t"
#           f"{record.prior_slot_time_end}\t\t")
# print()
# all_slots_records_by_month = get_slots_from_now_for_month(
#     year=year, month=month,
#     master_id=master_id
# )
# for record in all_slots_records_by_month:
#     print(f"{record.id}\t\t"
#           f"{record.day_of_month}\t\t"
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
