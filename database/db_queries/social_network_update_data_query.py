from database.db_connection import DBConnection
from database.db_engine_url import db_engine_url

from database.db_models.social_model import Social
from database.db_utilities.model_object_update import update_object
from telegram.params.button_social_networks import SOCIAL_NETWORK

manager = DBConnection(db_url=db_engine_url)


def social_network_update_data(
        social_network_id: int,
        social_network_name: str,
        social_network_url: str | None,
        social_network_username: str
):
    with manager as session:
        social_network_obj = session.query(Social).filter(
            Social.id == social_network_id).first()

        for attr_name, attr_value in vars(SOCIAL_NETWORK).items():
            if attr_name.startswith('__'):
                continue

            if isinstance(attr_value, tuple):
                name, url = attr_value

                if name == social_network_name:
                    social_network_url = url + social_network_username
                    break

            elif isinstance(attr_value, str):
                social_network_url = None
                break


        data = {
            'name': social_network_name,
            'url': social_network_url,
            'social_username': social_network_username
        }

        update_object(
            obj=social_network_obj,
            data=data,
            session=session
        )
