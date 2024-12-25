from typing import Optional

from sqlalchemy.orm import Session

from database.db_models.work_time_model import WorkTime


def get_worktime_obj_by_id_session(worktime_slot_id: int,
                                   ongoing_session: Session
                                   ) -> Optional[WorkTime]:
    work_times_slot_obj = ongoing_session.query(WorkTime).filter(
        WorkTime.id == worktime_slot_id).first()

    return work_times_slot_obj
