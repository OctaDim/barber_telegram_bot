from database.db_connection import DBConnection
from database.db_engine_url import db_engine_url

from database.db_models.social_model import Social
from database.db_models.user_model import User
from database.db_queries.user_obj_by_telegram_id import get_user_by_telegram_id_in_session

manager = DBConnection(db_url=db_engine_url)


def create_social_network(
        social_network: str,
        username_social_network: str,
        url_social_network: str,
        telegram_id: int
):
    if url_social_network:
        url_social_network = url_social_network + username_social_network

    with manager as session:
        user_obj = get_user_by_telegram_id_in_session(
            telegram_id=telegram_id,
            ongoing_session=session
        )

        social = Social(
            name=social_network,
            social_username=username_social_network,
            url=url_social_network,
            master_id=user_obj.user_masters.id
        )

        session.add(social)
        session.commit()
