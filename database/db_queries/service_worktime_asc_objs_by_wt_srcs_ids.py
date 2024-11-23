from typing import List, Type

from sqlalchemy.orm import Session

from database.db_models.association_service_worktime import (
    ServiceWorkTimeAssociation)


def get_service_worktime_asc_objs(worktime_id: list[int],
                                  services_ids: list[int],
                                  ongoing_session: Session
                                  ) -> List[Type[ServiceWorkTimeAssociation]]:
    service_worktime_asc_objs = ongoing_session.query(
        ServiceWorkTimeAssociation
    ).filter(
        ServiceWorkTimeAssociation.work_time_id == worktime_id,
        ServiceWorkTimeAssociation.service_id.in_(services_ids)
    ).all()

    return service_worktime_asc_objs
