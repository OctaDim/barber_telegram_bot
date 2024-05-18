from database.db_engine_url import db_engine_url
from database.db_connection import DBConnection

from database.db_models.phones_model import Phone
from database.db_models.services_model import Services

from telegram.params.buttons_main_menu import MAIN_MANU_ADMIN_PARAMS


manager = DBConnection(db_url=db_engine_url)


def get_admin_panel_btn_text():
    with manager as session:
        services = session.query(Services).all()
        phone = session.query(Phone).all()

        data = {
            'services': MAIN_MANU_ADMIN_PARAMS.ADD_SERVICES,
            'contacts': MAIN_MANU_ADMIN_PARAMS.ADD_CONTACTS,
        }

        if services:
            data['services'] = MAIN_MANU_ADMIN_PARAMS.CHANGE_SERVICES

        if phone:
            data['contacts'] = MAIN_MANU_ADMIN_PARAMS.CHANGE_CONTACTS

        return data


def add_services(data: dict):
    with manager as session:
        validate_data = {
            'name': data['name'],
            'description': data['description'],
            'price': data['price'],
        }

        session.add(Services(**validate_data))
        session.commit()
