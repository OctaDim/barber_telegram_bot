from datetime import datetime, date

from sqlalchemy import extract, func, cast, Row, Integer, case

from database.db_connection import DBConnection
from database.db_engine_url import db_engine_url
from database.db_models.work_time_model import WorkTime
from telegram.config.logging import LOGGING
from utilities.decorators_global import execution_time_decorator


@execution_time_decorator(in_seconds=True,
                          note="All slots_records from now for date",
                          exec_time_logging=LOGGING.EXECUTION_TIME)
def get_slots_from_now_for_date(required_date: date,
                                master_id: int = None,
                                reserved: bool = False,
                                active: bool = True,
                                admin_only: bool = False) -> list[Row]:
    with (DBConnection(db_url=db_engine_url) as session):
        slot_records_for_date = session.query(
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
                order_by=WorkTime.time_start).label("prior_slot_time_end"),
            case(
                (WorkTime.time_start == func.lag(WorkTime.time_end).over(
                    order_by=WorkTime.time_start), True),
                else_=False).label("continuing")
        ).filter(
            WorkTime.time_start >= datetime.now(),
            func.date(WorkTime.time_start) == required_date,
            WorkTime.active.is_(active),
            WorkTime.reserved.is_(reserved),
            WorkTime.admin_only.is_(admin_only),
            WorkTime.master_id == master_id
        ).order_by(
            "time_start",
            "master_id"
        ).all()

        return slot_records_for_date

# ##################### TEST CODE ######################################
# ######################################################################
# YEAR = 2024
# MONTH = 10
# DAY = 22
# test_date = datetime(year=YEAR, month=MONTH, day=DAY)
# days_records = get_slots_from_now_for_date(required_date=test_date,
#                                            master_id=None)
# for record in days_records:
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
# ######################################################################
# ##################### END TEST CODE ##################################
