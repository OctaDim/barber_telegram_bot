from database.db_engine import url_engine
from database.db_connection import DBConnection

from database.db_models.company import (
    Services
)


manager = DBConnection(db_url=url_engine)


def get_service():
    with manager as session:
        data = session.query(Services).all()

        return data


