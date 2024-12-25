from datetime import datetime, date
from typing import Union, Optional, Tuple, List

from sqlalchemy import extract, func, cast, Integer, case

from database.db_connection import DBConnection
from database.db_engine_url import db_engine_url
from database.db_models.master_model import Master
from database.db_models.service_model import Service
from database.db_models.user_model import User
from database.db_models.work_time_model import WorkTime
from database.db_utilities.create_order_by_partial_query import (
    create_order_by_partial_query)
from telegram.config.logging import LOGGING
from utilities.decorators_global import execution_time_decorator


@execution_time_decorator(in_seconds=True,
                          note="All slots_records from now for date",
                          exec_time_logging=LOGGING.EXECUTION_TIME)
def get_slots_from_now_for_date_query(
        required_date: date,
        worktime_id: Union[int, "all"] = "all",
        master_id: Union[int, "all"] = "all",
        masters_ids_list: Union[List[int], "all"] = "all",
        work_time_client_id: Union[int, "all"] = "all",
        work_time_services_ids: Union[List[int], "all"] = "all",
        reserved: Union[bool, "all"] = "all",
        active: Union[bool, "all"] = "all",
        admin_only: Union[bool, "all"] = "all",
        order_by_fields: Optional[Union[str, Tuple[str, ...], None]] = (
                "master_id", "time_start",)
) -> list[WorkTime]:
    with (DBConnection(db_url=db_engine_url) as session):
        base_query = session.query(
            Master.full_name.label("master_fullname"),
            WorkTime.id,
            cast(extract(
                "DAY", WorkTime.time_start), Integer).label("day_of_month"),
            WorkTime.master_id,
            WorkTime.time_start,
            WorkTime.time_end,
            WorkTime.slot_duration,
            # (WorkTime.time_end - WorkTime.time_start).label("slot_duration"),
            WorkTime.active,
            WorkTime.reserved,
            func.lag(WorkTime.time_end).over(
                partition_by=WorkTime.master_id,
                order_by=(
                    WorkTime.master_id,
                    WorkTime.time_start)
            ).label("prior_slot_time_end"),

            # ##### For the future
            # case((WorkTime.time_start == func.lag(WorkTime.time_end).over(
            #     partition_by=(
            #         WorkTime.master_id),
            #     order_by=(
            #         WorkTime.master_id,
            #         WorkTime.time_start)), True),
            #      else_=False
            #      ).label("slots_time_continuing")

        ).join(
            Master, Master.id == WorkTime.master_id)

        filter_query = base_query.filter(
            WorkTime.time_start >= datetime.now(),
            func.date(WorkTime.time_start) == required_date)

        if worktime_id != "all":
            filter_query = filter_query.filter(
                WorkTime.id == worktime_id)

        if master_id != "all":
            filter_query = filter_query.filter(
                WorkTime.master_id == master_id)

        if masters_ids_list != "all":
            filter_query = filter_query.filter(
                WorkTime.master_id.in_(masters_ids_list))

        if work_time_client_id != "all":
            filter_query = filter_query.filter(
                WorkTime.work_time_clients.any(
                    User.id == work_time_client_id))

        if work_time_services_ids != "all":
            filter_query = filter_query.filter(
                WorkTime.work_time_services.any(
                    Service.id.in_(work_time_services_ids)))

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

        slot_records_for_date = order_query.all()
        return slot_records_for_date

# ##################### TEST CODE ######################################
# ######################################################################
# import database.db_imports_initialization
# YEAR = 2024
# MONTH = 11
# DAY = 19
# test_date = datetime(year=YEAR, month=MONTH, day=DAY)
#
# days_records = get_slots_from_now_for_date_query(
#     required_date=test_date,
#     # master_id=1,
#     # masters_ids_list=[1],
#     masters_ids_list=[1, 2, 3],
#     order_by_fields=("master_id", "time_start"),
#     active=True,
#     reserved=False,
#     admin_only=False,
# )
# for record in days_records:
#     print(f"{record.id}\t"
#           f"{record.day_of_month}\t\t"
#           f"{record.master_id}\t\t"
#           # f"{record.active}\t"
#           # f"{record.reserved}\t"
#           f"{record.time_start}\t\t"
#           f"{record.time_end}\t"
#           f"{record.slot_duration}\t\t"
#           f"{record.prior_slot_time_end}\t\t\t\t\t"
#           f"{record.slots_time_continuing}\t\t"
#           # f"{record.prior_slot_master_id}\t\t"
#           # f"{record.master_id_continuing}\t\t"
#           # f"{record.master_id_continuing}\t\t"
#           )
# print()
# ######################################################################
# ##################### END TEST CODE ##################################
