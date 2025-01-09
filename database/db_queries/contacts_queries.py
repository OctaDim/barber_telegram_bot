from typing import Optional

from database.db_connection import DBConnection
from database.db_engine_url import db_engine_url
from database.db_models.address_model import Address
from database.db_models.phone_model import Phone
from database.db_models.social_model import Social
from telegram.config.logging import LOGGING
from utilities.decorators_global import execution_time_decorator


@execution_time_decorator(in_seconds=True, note="Social, phones, address",
                          exec_time_logging=LOGGING.EXECUTION_TIME)
def get_company_contacts(company_id: int = None) -> Optional[dict]:
    with DBConnection(db_url=db_engine_url) as session:
        if not company_id:
            socials = session.query(
                Social.name, Social.url, Social.social_username).all()
            phones = session.query(Phone.number).all()
            address = session.query(Address.street, Address.url).all()

        else:
            socials = session.query(
                Social.name, Social.url, Social.social_username
            ).filter(
                Social.company_id == company_id).all()

            phones = session.query(Phone.number).filter(
                Phone.company_id == company_id).all()

            address = session.query(Address.street, Address.url).filter(
                Address.company_id == company_id).all()

        contacts_data = ""
        if address or socials or phones:
            contacts_data = {"socials": [social for social in socials],
                             "phones": [phone for phone in phones],
                             "addresses": [address for address in address]}
        return contacts_data
