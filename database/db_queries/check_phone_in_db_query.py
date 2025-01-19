from database.db_connection import DBConnection
from database.db_engine_url import db_engine_url

from database.db_models.phone_model import Phone


manager = DBConnection(db_url=db_engine_url)


def check_phone_in_db(phone: str):
    with manager as session:
        phone_obj = session.query(Phone).filter(
            Phone.number == phone).one_or_none()

        return phone_obj
