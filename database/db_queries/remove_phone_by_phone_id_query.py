from database.db_connection import DBConnection
from database.db_engine_url import db_engine_url

from database.db_models.phone_model import Phone


manager = DBConnection(db_url=db_engine_url)


def remove_phone_by_phone_id(phone_id: int):
    with manager as session:
        phone_obj = session.query(Phone).filter(
            Phone.id == phone_id).one_or_none()

        session.delete(phone_obj)
        session.commit()
