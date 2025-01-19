from database.db_connection import DBConnection
from database.db_engine_url import db_engine_url

from database.db_models.social_model import Social
from database.db_queries.user_obj_by_telegram_id import get_user_by_telegram_id_in_session

manager = DBConnection(db_url=db_engine_url)


def get_all_social_networks_by_masters(telegram_id: int):
    with manager as session:
        user_obj = get_user_by_telegram_id_in_session(
            telegram_id=telegram_id,
            ongoing_session=session
        )

        data = session.query(Social).filter(
            Social.master_id == user_obj.user_masters.id).all()

        return data
