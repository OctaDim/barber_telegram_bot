from typing import Optional

from database.db_connection import DBConnection
from database.db_engine_url import db_engine_url
from database.db_models.work_time_model import WorkTime


def get_worktime_slot_by_id(worktime_slot_id: int) -> Optional[WorkTime]:
    with DBConnection(db_url=db_engine_url) as session:
        work_times_lot_by_id = session.query(
            WorkTime).filter(WorkTime.id == worktime_slot_id).first()

        return work_times_lot_by_id
