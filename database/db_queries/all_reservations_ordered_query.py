from datetime import datetime
from typing import List, Union, Tuple

from sqlalchemy import UnaryExpression

from database.db_connection import DBConnection
from database.db_engine_url import db_engine_url
from database.db_models.reservation_model import Reservation
from database.db_utilities.create_order_by_partial_query import (
    create_order_by_partial_query)
from telegram.config.logging import LOGGING
from utilities.decorators_global import execution_time_decorator


@execution_time_decorator(in_seconds=True,
                          note="All reservations by user_id",
                          exec_time_logging=LOGGING.EXECUTION_TIME)
def get_all_reservations_ordered(
        client_user_id: Union[int, "all"] = "all",
        cancelled_by_client: Union[bool, "all"] = "all",
        cancelled_by_admin: Union[bool, "all"] = "all",
        show_completed_reservations: bool = True,
        order_by_fields: Union[
            str, Tuple[str, ...], UnaryExpression, Tuple[UnaryExpression, ...],
            None] = (Reservation.reserved_interval_time_start.desc(),)
) -> List[Reservation]:
    with DBConnection(db_url=db_engine_url) as session:
        base_query = session.query(Reservation)

        filter_query = base_query
        if not show_completed_reservations:
            filter_query = filter_query.filter(
                Reservation.reserved_interval_time_start > datetime.now())

        if client_user_id != "all":
            filter_query = filter_query.filter(
                Reservation.client_user_id == client_user_id)

        if cancelled_by_client != "all":
            filter_query = filter_query.filter(
                Reservation.cancelled_by_client.is_(cancelled_by_client))

        if cancelled_by_admin != "all":
            filter_query = filter_query.filter(
                Reservation.cancelled_by_admin.is_(cancelled_by_admin))

        order_query = create_order_by_partial_query(
            model_class=Reservation,
            prior_filter_query=filter_query,
            order_by_fields=order_by_fields)

        all_reservations_objs = order_query.all()
    return all_reservations_objs
