from typing import List, Union, Optional, Tuple

from database.db_connection import DBConnection
from database.db_engine_url import db_engine_url
from database.db_models.service_model import Service
from database.db_utilities.create_order_by_partial_query import (
    create_order_by_partial_query)


def get_all_services_ordered(
        category_id: Union[int, "all"] = "all",
        master_id: Union[int, "all"] = "all",
        active: Union[bool, "all"] = "all",
        order_by_fields: Optional[Union[str, Tuple[str, ...]]] = ("name",)
) -> List[Service]:
    with DBConnection(db_url=db_engine_url) as session:
        base_query = session.query(Service)

        filter_query = base_query
        if category_id != "all":
            filter_query = filter_query.filter(
                Service.category_id == category_id)

        if master_id != "all":
            filter_query = filter_query.filter(
                Service.master_id == master_id)

        if active != "all":
            filter_query = base_query.filter(
                Service.active.is_(active))

        order_query = create_order_by_partial_query(
            model_class=Service,
            prior_filter_query=filter_query,
            order_by_fields=order_by_fields)

        all_services_objs = order_query.all()
        return all_services_objs

# ##################### TEST CODE ######################################
# ######################################################################
# order_by_fields = ("name", "id", "master_id", "category_id")
# # order_by_fields = ("id", "name", "master_id", "category_id")
#
# all_services_objects = get_all_services(
#     order_by_fields=order_by_fields)
# for service in all_services_objects:
#     print(service.id, service.name, service.master_id, service.category_id)
# print()
#
# all_services_objects = get_all_services(active=False)
# for service in all_services_objects:
#     print(service.id, service.active)
# print()
#
# all_services_objects = get_all_services()
# for service in all_services_objects:
#     print(service.id, service.active)
# print()
# ######################################################################
# ##################### END TEST CODE ##################################
