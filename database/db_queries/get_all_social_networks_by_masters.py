from database.db_connection import DBConnection
from database.db_engine_url import db_engine_url

from database.db_models.social_model import Social

manager = DBConnection(db_url=db_engine_url)


def get_all_social_networks_by_masters():
    with manager as session:
        data = session.query(Social).all()

        return data
