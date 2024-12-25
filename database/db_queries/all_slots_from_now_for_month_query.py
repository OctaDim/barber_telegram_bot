from datetime import datetime
from typing import Union, Optional, Tuple, List

from sqlalchemy import extract, func, cast, Integer

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
def get_slots_from_now_for_month_query(
        year: int,
        month: int,
        worktime_id: Union[int, "all"] = "all",
        master_id: Union[int, "all"] = "all",
        masters_ids_list: Union[List[int], "all"] = "all",
        work_time_client_id: Union[int, "all"] = "all",
        reserved: Union[bool, "all"] = "all",
        active: Union[bool, "all"] = "all",
        admin_only: Union[bool, "all"] = "all",
        order_by_fields: Optional[Union[str, Tuple[str, ...], None]] = (
                "master_id", "time_start",)
) -> list[WorkTime]:
    with DBConnection(db_url=db_engine_url) as session:
        base_query = session.query(
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
                partition_by=(
                    extract("DAY", WorkTime.time_start),
                    WorkTime.master_id),
                order_by=(
                    extract("DAY", WorkTime.time_start),
                    WorkTime.master_id,
                    WorkTime.time_start)
            ).label("prior_slot_time_end"),

            # ##### For the future
            # case((WorkTime.time_start == func.lag(WorkTime.time_end).over(
            #     partition_by=(
            #         extract("DAY", WorkTime.time_start),
            #         WorkTime.master_id),
            #     order_by=(
            #         extract("DAY", WorkTime.time_start),
            #         WorkTime.master_id,
            #         WorkTime.time_start)), True),
            #      else_=False
            #      ).label("slots_time_continuing")
        )

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

        if masters_ids_list != "all":
            filter_query = filter_query.filter(
                WorkTime.master_id.in_(masters_ids_list))

        if work_time_client_id != "all":
            filter_query = filter_query.filter(
                WorkTime.work_time_clients.any(
                    User.id == work_time_client_id))

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
# import database.db_imports_initialization
#
# all_slots_records_by_month = get_slots_from_now_for_month_query(
#     year=2024,
#     month=11,
#     # master_id=1,
#     # masters_ids_list=[1],
#     masters_ids_list=[1, 2, 3],
#     order_by_fields=("master_id", "time_start"),
#     active=True,
#     reserved=False,
#     admin_only=False,
# )
# for record in all_slots_records_by_month:
#     print(f"{record.id}\t\t"
#           f"{record.day_of_month}\t\t"
#           f"{record.master_id}\t\t"
#           # f"{record.active}\t\t"
#           # f"{record.reserved}\t\t"
#           f"{record.time_start}\t\t"
#           f"{record.time_end}\t\t"
#           f"{record.slot_duration}\t\t"
#           f"{record.prior_slot_time_end}\t\t\t\t\t"
#           f"{record.slots_time_continuing}\t\t"
#           # f"{record.master_id_continuing}\t\t"
#           )
# print()
# ######################################################################
# ##################### END TEST CODE ##################################
