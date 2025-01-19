from database.db_connection import DBConnection
from database.db_engine_url import db_engine_url

from database.db_models.address_model import Address
from database.db_queries.user_obj_by_telegram_id import get_user_by_telegram_id_in_session

manager = DBConnection(db_url=db_engine_url)


def remove_address_obj(telegram_id: int):
    with manager as session:
        user_obj = get_user_by_telegram_id_in_session(
            telegram_id=telegram_id,
            ongoing_session=session
        )

        obj = session.query(Address).filter(
            Address.master_id == user_obj.user_masters.id).one_or_none()

        if obj is None:
            return

        session.delete(obj)
        session.commit()
