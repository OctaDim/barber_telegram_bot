from database.db_connection import DBConnection
from database.db_engine_url import db_engine_url

from database.db_models.social_model import Social

manager = DBConnection(db_url=db_engine_url)


def get_social_network_by_id(social_network_id: int):
    with manager as session:
        obj = session.query(Social).filter(
            Social.id == social_network_id).first()

        return obj
