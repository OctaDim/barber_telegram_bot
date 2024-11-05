from database.db_connection import DBConnection
from database.db_engine_url import db_engine_url
from database.db_models.user_model import User


def get_master_id_by_telegram_id(telegram_id: int, master_object=None):
    with DBConnection(db_url=db_engine_url) as session:
        user_obj = session.query(
            User).filter(User.telegram_id == telegram_id).first()

        master_id = user_obj.user_masters.id

        if master_object:
            master_obj = user_obj.user_masters

            return master_id, master_obj

        return master_id
