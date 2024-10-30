from typing import List, Type

from sqlalchemy.orm import Session

from database.db_models.service_model import Service


def get_unique_services_objs_by_ids_list(services_ids_list: list,
                                         ongoing_session: Session
                                         ) -> List[Type[Service]]:
    services_objs_list = ongoing_session.query(Service).filter(
        Service.id.in_(services_ids_list)).all()
    return services_objs_list


def get_non_unique_services_objs_by_ids_list(services_ids_list: list,
                                             ongoing_session: Session
                                             ) -> List[Type[Service]]:
    services_objects_list = []
    for cur_service_id in services_ids_list:
        cur_service_object = ongoing_session.query(Service).filter(
            Service.id == cur_service_id).first()

        if cur_service_object:
            services_objects_list.append(cur_service_object)
    return services_objects_list
