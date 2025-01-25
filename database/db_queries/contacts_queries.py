from typing import Optional, Tuple, Union

from sqlalchemy import UnaryExpression

from database.db_connection import DBConnection
from database.db_engine_url import db_engine_url
from database.db_models.address_model import Address
from database.db_models.phone_model import Phone
from database.db_models.social_model import Social
from database.db_utilities.create_order_by_partial_query import (
    create_order_by_partial_query)
from telegram.config.logging import LOGGING
from utilities.decorators_global import (
    execution_time_decorator)


@execution_time_decorator(in_seconds=True, note="Social, phones, address",
                          exec_time_logging=LOGGING.EXECUTION_TIME)
def get_company_contacts(
        company_id: Union[int, "all"] = "all",
        socials_order_by_fields: Union[
            str, Tuple[str, ...], UnaryExpression,
            Tuple[UnaryExpression, ...], None] = ("sort_index", "name",),
        phones_order_by_fields: Union[
            str, Tuple[str, ...], UnaryExpression,
            Tuple[UnaryExpression, ...], None] = ("sort_index", "name",),
        address_order_by_fields: Union[
            str, Tuple[str, ...], UnaryExpression,
            Tuple[UnaryExpression, ...], None] = ("sort_index", "name",)
) -> Optional[dict]:
    with (DBConnection(db_url=db_engine_url) as session):
        if company_id == "all":
            base_socials_query = session.query(Social)
            base_phones_query = session.query(Phone)
            base_address_query = session.query(Address)

        else:
            base_socials_query = session.query(Social).filter(
                Social.company_id == company_id)

            base_phones_query = session.query(Phone).filter(
                Phone.company_id == company_id)

            base_address_query = session.query(Address).filter(
                Address.company_id == company_id)

        order_socials_query = create_order_by_partial_query(
            model_class=Social,
            prior_filter_query=base_socials_query,
            order_by_fields=socials_order_by_fields)
        socials_objs = order_socials_query.all()

        order_phones_query = create_order_by_partial_query(
            model_class=Phone,
            prior_filter_query=base_phones_query,
            order_by_fields=phones_order_by_fields)
        phones_objs = order_phones_query.all()

        order_address_query = create_order_by_partial_query(
            model_class=Address,
            prior_filter_query=base_address_query,
            order_by_fields=address_order_by_fields)
        address_objs = order_address_query.all()

        if address_objs or socials_objs or phones_objs:
            contacts_data = {
                "socials": [social_obj for social_obj in socials_objs],
                "phones": [phone_obj for phone_obj in phones_objs],
                "addresses": [address_obj for address_obj in address_objs]}
            return contacts_data

        return None
