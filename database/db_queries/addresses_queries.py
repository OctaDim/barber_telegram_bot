from typing import Optional, Tuple, Union

from sqlalchemy import UnaryExpression

from database.db_connection import DBConnection
from database.db_engine_url import db_engine_url
from database.db_models.address_model import Address
from database.db_utilities.create_order_by_partial_query import create_order_by_partial_query
from telegram.config.logging import LOGGING
from utilities.decorators_global import execution_time_decorator


@execution_time_decorator(in_seconds=True, note="Social, phones, address",
                          exec_time_logging=LOGGING.EXECUTION_TIME)
def get_company_addresses_for_maps(
        company_id: Union[int, "all"] = "all",
        address_order_by_fields: Union[
            str, Tuple[str, ...], UnaryExpression,
            Tuple[UnaryExpression, ...], None] = ("sort_index", "name",)
) -> Optional[dict]:
    with (DBConnection(db_url=db_engine_url) as session):
        if company_id == "all":
            base_address_query = session.query(Address)
        else:
            base_address_query = session.query(Address).filter(
                Address.company_id == company_id)

        order_address_query = create_order_by_partial_query(
            model_class=Address,
            prior_filter_query=base_address_query,
            order_by_fields=address_order_by_fields)
        address_objs = order_address_query.all()

        if address_objs:
            addresses_data = {
                "addresses": [address_obj for address_obj in address_objs]}
            return addresses_data

        return None
