from database.db_engine import url_engine
from database.db_connection import DBConnection

from database.db_models.company import (
    Services,
    Phone
)

from telegram.params.buttons_main_menu import MAIN_MANU_ADMIN_PARAMS


manager = DBConnection(db_url=url_engine)


def get_btn_admin_panel():
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
