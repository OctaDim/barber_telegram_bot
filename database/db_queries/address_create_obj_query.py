from database.db_connection import DBConnection
from database.db_engine_url import db_engine_url

from database.db_models.address_model import Address
from database.db_utilities.model_object_update import update_object

manager = DBConnection(db_url=db_engine_url)


def create_address_db_obj(street: str, url: str):
    with manager as session:
        obj = session.query(Address).one_or_none()

        if obj is None:
            new_obj = Address(street=street, url=url)

            session.add(new_obj)
            session.commit()

            return

        data = {
            'street': street,
            'url': url
        }

        update_object(obj=obj, data=data, session=session)
