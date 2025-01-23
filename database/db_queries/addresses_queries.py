from typing import Optional, Union

from database.db_connection import DBConnection
from database.db_engine_url import db_engine_url
from database.db_models.address_model import Address
from telegram.config.logging import LOGGING
from utilities.decorators_global import execution_time_decorator


@execution_time_decorator(in_seconds=True, note="Social, phones, address",
                          exec_time_logging=LOGGING.EXECUTION_TIME)
def get_company_addresses_for_maps(
        company_id: Union[int, "all"] = "all") -> Optional[dict]:
    with DBConnection(db_url=db_engine_url) as session:
        if company_id == "all":
            address = session.query(Address.street, Address.url).all()
        else:
            address = session.query(Address.street, Address.url).filter(
                Address.company_id == company_id).all()

        if address:
            addresses_data = {"addresses": [address for address in address]}
            return addresses_data

        return None
