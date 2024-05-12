

from database.db_engine import url_engine
from database.db_connection import DBConnection

from database.db_models.company import (
    Services,
    Phone,
    Socials,
    Address
)



manager = DBConnection(db_url=url_engine)


def get_service():
    with manager as session:
        data = session.query(Services).all()

        return data


def get_about_info_company():
    with manager as session:
        address = session.query(Address).first()
        socials = session.query(Socials).all()
        phones = session.query(Phone).all()

        if address and socials and phones:
            data = {
                'address': [f'<a href="{address.url}">{address.street}</a>\n'],
                'phone': [phone.number.international for phone in phones],
                'socials': [f'<a href="{social.url}">{social.name}</a>\n' for social in socials],
            }

            return data

        return None
