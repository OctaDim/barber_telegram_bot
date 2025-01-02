from database.db_connection import DBConnection
from database.db_engine_url import db_engine_url

from database.db_models.address_model import Address


manager = DBConnection(db_url=db_engine_url)


def remove_address_obj():
    with manager as session:
        obj = session.query(Address).one_or_none()
        print(obj)
        if obj is None:
            return

        session.delete(obj)
        session.commit()
