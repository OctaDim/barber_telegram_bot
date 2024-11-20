from typing import Optional

from database.db_connection import DBConnection
from database.db_engine_url import db_engine_url
from database.db_models.user_model import User


def get_user_obj_by_telegram_id(telegram_id: int) -> Optional[User]:
    with DBConnection(db_url=db_engine_url) as session:
        user_obj_by_telegram_id = session.query(User).filter(
            User.telegram_id == telegram_id).first()

        return user_obj_by_telegram_id
