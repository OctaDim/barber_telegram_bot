from database.db_connection import DBConnection
from database.db_engine_url import db_engine_url

from database.db_models.social_model import Social

manager = DBConnection(db_url=db_engine_url)


def create_social_network(
        social_network: str,
        username_social_network: str,
        url_social_network: str
):
    if url_social_network:
        url_social_network = url_social_network + username_social_network

    with manager as session:
        social = Social(
            name=social_network,
            social_username=username_social_network,
            url=url_social_network
        )

        session.add(social)
        session.commit()
