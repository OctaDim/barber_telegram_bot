from typing import List, Set, Union

from database.db_connection import DBConnection
from database.db_engine_url import db_engine_url
from database.db_models.service_model import Service


def get_masters_ids_common_for_services(
        services_ids_list: List[int]
) -> List[int]:
    with DBConnection(db_url=db_engine_url) as session:
        service_objs_list = session.query(Service).filter(
            Service.id.in_(services_ids_list)).all()

        masters_objs_per_service = []
        for service_obj in service_objs_list:
            masters_objs_per_service.append(set(service_obj.service_masters))

        common_masters_objs = set.intersection(*masters_objs_per_service)
        if not common_masters_objs:
            return []

        common_masters_ids = [master.id for master in common_masters_objs]
        return common_masters_ids
