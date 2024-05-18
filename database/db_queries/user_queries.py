from database.db_engine_url import db_engine_url
from database.db_connection import DBConnection

from database.db_models.address_model import Address
from database.db_models.socials_model import Socials
from database.db_models.phones_model import Phone
from database.db_models.services_model import Services

manager = DBConnection(db_url=db_engine_url)


def get_services_list():
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
