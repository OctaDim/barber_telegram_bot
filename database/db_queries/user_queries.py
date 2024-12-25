from typing import List, Optional

from database.db_connection import DBConnection
from database.db_engine_url import db_engine_url
from database.db_models.service_model import Service
from database.db_models.user_model import User

manager = DBConnection(db_url=db_engine_url)


def get_services_list() -> [List[Service]]:
    with manager as session:
        data = session.query(Service).all()
        return data
