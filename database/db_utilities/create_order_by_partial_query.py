from typing import Optional, Tuple, Type, Union, Any

from sqlalchemy.orm import Query

from database.db_connection import Base


def create_order_by_partial_query(
        model_class: Union[Type[Base], Type[Any]],
        prior_filter_query: Query,
        order_by_fields: Optional[Union[str, Tuple[str, ...]]] = ("id",)):

    order_query = prior_filter_query

    if isinstance(order_by_fields, str):
        order_by_fields_validated = tuple(order_by_fields)
    else:
        order_by_fields_validated = order_by_fields

    if order_by_fields:
        for order_field in order_by_fields_validated:
            if hasattr(model_class, order_field):
                order_query = order_query.order_by(order_field)
            else:
                print(f"\tTEST INFO: Order by '{order_field}' skipped because "
                      f"attribute was not found in model class '{model_class}'\n")
    return order_query
