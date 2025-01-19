from database.db_connection import DBConnection
from database.db_engine_url import db_engine_url

from database.db_models.phone_model import Phone
from database.db_utilities.model_object_update import update_object

manager = DBConnection(db_url=db_engine_url)


def update_phone_by_phone_id(phone_id: int, phone: str,):
    with manager as session:
        phone_obj = session.query(Phone).filter(
            Phone.id == phone_id).first()

        data = {'number': phone}

        update_object(data=data, obj=phone_obj, session=session)
