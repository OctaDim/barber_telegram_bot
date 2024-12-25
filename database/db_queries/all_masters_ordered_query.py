from typing import List, Union, Tuple

from sqlalchemy import UnaryExpression

from database.db_connection import DBConnection
from database.db_engine_url import db_engine_url
from database.db_models.master_model import Master
from database.db_utilities.create_order_by_partial_query import (
    create_order_by_partial_query)
from telegram.config.logging import (
    LOGGING)
from utilities.decorators_global import (
    execution_time_decorator)


@execution_time_decorator(in_seconds=True,
                          note="All masters ordered query",
                          exec_time_logging=LOGGING.EXECUTION_TIME)
def get_all_masters_ordered(
        master_id: Union[int, "all"] = "all",
        category_id: Union[int, "all"] = "all",
        user_id: Union[int, "all"] = "all",
        active: Union[bool, "all"] = "all",
        order_by_fields: Union[
            str, Tuple[str, ...], UnaryExpression, Tuple[UnaryExpression, ...],
            None] = ("full_name",)
) -> List[Master]:
    with DBConnection(db_url=db_engine_url) as session:
        base_query = session.query(Master)

        filter_query = base_query
        if master_id != "all":
            filter_query = filter_query.filter(
                Master.id == master_id)

        if category_id != "all":
            filter_query = filter_query.filter(
                Master.category_id == category_id)

        if user_id != "all":
            filter_query = filter_query.filter(
                Master.user_id == user_id)

        if active != "all":
            filter_query = filter_query.filter(
                Master.active.is_(active))

        order_query = create_order_by_partial_query(
            model_class=Master,
            prior_filter_query=filter_query,
            order_by_fields=order_by_fields)

        all_masters_objs = order_query.all()
        return all_masters_objs

# ##################### TEST CODE ######################################
# ######################################################################
# order_by_fields = ("category_id", "name", "id", "user_id")
# order_by_fields = ("id", "category_id", "name", "user_id")
# order_by_fields = ("name", "category_id", "id", "user_id")
#
# order_by_fields = "category_id"
# category_id = 5
#
# all_masters_objects = get_all_masters_ordered(
#     order_by_fields=order_by_fields)
# for master in all_masters_objects:
#     print(master.id, master.first_name, master.user_id, master.category_id, master.active)
# print()
#
# all_masters_objects = get_all_masters_ordered(active=False)
# for master in all_masters_objects:
#     print(master.id, master.first_name, master.user_id, master.category_id, master.active)
# print()
#
# selected_category_id = 7
#
# all_masters_objects = get_all_masters_ordered(
#     active=True,
#     category_id=selected_category_id,
#     order_by_fields=("last_name", "first_name", "middle_name",)
# )
#
# for master in all_masters_objects:
#     print("######", master.id, master.first_name, master.user_id, master.category_id, master.active)
# print()
# ######################################################################
# ##################### END TEST CODE ##################################
