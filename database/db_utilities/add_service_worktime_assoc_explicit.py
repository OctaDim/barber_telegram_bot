from datetime import datetime

from sqlalchemy.orm import Session

from database.db_models.association_service_worktime import ServiceWorkTimeAssociation


def add_service_worktime_association(selected_services_ids: list,
                                     worktime_slot_id: int,
                                     current_user_id: int,
                                     ongoing_session: Session) -> None:
    """Explicit adding assoc to save repeated services for each work time"""
    for service_id in selected_services_ids:
        service_worktime_assoc = ServiceWorkTimeAssociation(
            service_id=service_id,
            work_time_id=worktime_slot_id,
            updated=datetime.now(),
            creator_id=current_user_id)

        ongoing_session.add(service_worktime_assoc)
