from typing import List, Union, Optional, Tuple

from database.db_connection import DBConnection
from database.db_engine_url import db_engine_url
from database.db_models.category_model import Category
from database.db_utilities.create_order_by_partial_query import (
    create_order_by_partial_query)


def get_all_categories_ordered(
        active: Union[bool, "all"] = "all",
        order_by_fields: Optional[Union[str, Tuple[str, ...]]] = ("name",)
) -> List[Category]:
    with DBConnection(db_url=db_engine_url) as session:
        base_query = session.query(Category)

        filter_query = base_query
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
