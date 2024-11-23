from typing import List, Union, Tuple

from sqlalchemy import UnaryExpression
from sqlalchemy.orm import joinedload

from database.db_connection import DBConnection
from database.db_engine_url import db_engine_url
from database.db_models.master_model import Master
from database.db_models.service_model import Service
from database.db_utilities.create_order_by_partial_query import (
    create_order_by_partial_query)
from telegram.config.logging import (LOGGING)
from utilities.decorators_global import (execution_time_decorator)


@execution_time_decorator(in_seconds=True,
                          note="All services ordered with service masters query",
                          exec_time_logging=LOGGING.EXECUTION_TIME)
def get_all_services_ordered(
        service_id: Union[int, "all"] = "all",
        category_id: Union[int, "all"] = "all",
        master_id: Union[int, "all"] = "all",
        active: Union[bool, "all"] = "all",
        order_by_fields: Union[
            str, Tuple[str, ...], UnaryExpression, Tuple[UnaryExpression, ...],
            None] = ("name", "price",)
) -> List[Service]:
    with DBConnection(db_url=db_engine_url) as session:
        base_query = session.query(Service).options(
            # joined_load(Master.master_categories) for masters by category via services
            joinedload(Service.service_masters).joinedload(Master.master_categories)
        )

        filter_query = base_query
        if service_id != "all":
            filter_query = filter_query.filter(
                Service.id == service_id)

        if category_id != "all":
            filter_query = filter_query.filter(
                Service.category_id == category_id)

        if master_id != "all":
            filter_query = filter_query.filter(
                Service.service_masters.any(Master.id == master_id))

        if active != "all":
            filter_query = filter_query.filter(
                Service.active.is_(active))

        order_query = create_order_by_partial_query(
            model_class=Service,
            prior_filter_query=filter_query,
            order_by_fields=order_by_fields)

        all_services_objs = order_query.all()
        return all_services_objs

# ##################### TEST CODE ######################################
# ######################################################################
# import database.db_imports_initialization
#
# order_by_fields = ("name", "id", "master_id", "category_id")
# # order_by_fields = ("id", "name", "master_id", "category_id")
#
# all_services_objects = get_all_services_ordered(
#     order_by_fields=order_by_fields)
# for service_obj in all_services_objects:
#     print(f""
#           f"{service_obj.id}\t\t"
#           f"{service_obj.price}\t\t"
#           f"{service_obj.category_id}\t\t"
#           f"{service_obj.name}\t\t"
#           f"")
# print()
########################################################################
# ##################### END TEST CODE ##################################


# ##################### FOR THE FUTURE #################################
# def get_services_by_category_master(
#         category_id: int,
#         master_id: int,
#         active: bool = True
# ) -> List[Service]:
#     with DBConnection(db_url=db_engine_url) as session:
#         filtered_services_records = session.query(Service).filter(
#             Service.category_id == category_id,
#             Service.service_masters.any(Master.id == master_id),
#             Service.active.is_(active)
#         ).options(
#             joinedload(Service.service_masters)
#         ).order_by(
#             "name", "price"
#         ).all()
#         return filtered_services_records
#
# def get_services_by_master(
#         master_id: int,
#         active: bool = True
# ) -> List[Service]:
#     with DBConnection(db_url=db_engine_url) as session:
#         filtered_services_records = session.query(Service).filter(
#             Service.service_masters.any(Master.id == master_id),
#             Service.active.is_(active)
#         ).options(
#             joinedload(Service.service_masters)
#         ).order_by(
#             "name", "price"
#         ).all()
#         return filtered_services_records
#
# def get_services_by_category(
#         category_id: int,
#         active: bool = True
# ) -> List[Service]:
#     with DBConnection(db_url=db_engine_url) as session:
#         filtered_services_records = session.query(Service).filter(
#             Service.category_id == category_id,
#             Service.active.is_(active),
#         ).options(
#             joinedload(Service.service_masters)
#         ).order_by(
#             "name", "price"
#         ).all()
#         return filtered_services_records
