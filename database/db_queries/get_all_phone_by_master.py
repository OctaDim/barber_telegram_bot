from database.db_connection import DBConnection
from database.db_engine_url import db_engine_url

from database.db_models.phone_model import Phone

from database.db_queries.get_master_obj_by_telegram_id import get_master_id_by_telegram_id


manager = DBConnection(db_url=db_engine_url)


def get_all_phone_by_masters(telegram_id: int):
    with manager as session:
        _, master_obj = get_master_id_by_telegram_id(
            telegram_id=telegram_id,
            master_object=True
        )

        phones = session.query(Phone).filter(
            Phone.phone_masters.any(id=master_obj.id)).all()

        return phones
