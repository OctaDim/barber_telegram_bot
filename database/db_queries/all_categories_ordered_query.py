from typing import List, Union, Tuple

from sqlalchemy import UnaryExpression

from database.db_connection import DBConnection
from database.db_engine_url import db_engine_url
from database.db_models.category_model import Category
from database.db_utilities.create_order_by_partial_query import (
    create_order_by_partial_query)
from telegram.config.logging import (
    LOGGING)
from utilities.decorators_global import (
    execution_time_decorator)


@execution_time_decorator(in_seconds=True,
                          note="All categories ordered query",
                          exec_time_logging=LOGGING.EXECUTION_TIME)
def get_all_categories_ordered(
        category_id: Union[bool, "all"] = "all",
        active: Union[bool, "all"] = "all",
        order_by_fields: Union[
            str, Tuple[str, ...], UnaryExpression, Tuple[UnaryExpression, ...],
            None] = ("name",)
) -> List[Category]:
    with DBConnection(db_url=db_engine_url) as session:
        base_query = session.query(Category)

        filter_query = base_query
        if category_id != "all":
            filter_query = filter_query.filter(
                Category.id == category_id)

        if active != "all":
            filter_query = filter_query.filter(
                Category.active.is_(active))

        order_query = create_order_by_partial_query(
            model_class=Category,
            prior_filter_query=filter_query,
            order_by_fields=order_by_fields)

        all_categories_objs = order_query.all()
        return all_categories_objs

# ##################### TEST CODE ######################################
# ######################################################################
# all_categories_objs = get_all_categories(active=True)
# for category in all_categories_objs:
#     print(category.id, category.active)
# print()
#
# all_categories_objs = get_all_categories(active=False)
# for category in all_categories_objs:
#     print(category.id, category.active)
# print()
#
# all_categories_objs = get_all_categories()
# for category in all_categories_objs:
#     print(category.id, category.active)
# print()
# ######################################################################
# ##################### END TEST CODE ##################################
