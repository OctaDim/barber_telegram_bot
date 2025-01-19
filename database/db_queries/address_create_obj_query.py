from database.db_connection import DBConnection
from database.db_engine_url import db_engine_url

from database.db_models.address_model import Address
from database.db_queries.user_obj_by_telegram_id import get_user_by_telegram_id_in_session
from database.db_utilities.model_object_update import update_object

manager = DBConnection(db_url=db_engine_url)


def create_address_db_obj(street: str, url: str, telegram_id: int):
    with manager as session:
        user_obj = get_user_by_telegram_id_in_session(
            telegram_id=telegram_id,
            ongoing_session=session
        )

        obj = session.query(Address).filter(
            Address.master_id == user_obj.user_masters.id).one_or_none()

        if obj is None:
            new_obj = Address(
                street=street,
                url=url,
                master_id=user_obj.user_masters.id)

            session.add(new_obj)
            session.commit()

            return

        data = {
            'street': street,
            'url': url
        }

        update_object(obj=obj, data=data, session=session)
