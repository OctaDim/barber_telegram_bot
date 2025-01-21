from typing import List, Optional

from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

from database.db_connection import DBConnection
from database.db_engine_url import db_engine_url
from database.db_models.user_model import User


def get_user_obj_by_telegram_id(telegram_id: int) -> Optional[User]:
    with DBConnection(db_url=db_engine_url) as session:
        user_obj_by_telegram_id = session.query(User).filter(
            User.telegram_id == telegram_id).first()

        return user_obj_by_telegram_id


def get_user_by_telegram_id_in_session(telegram_id: int,
                                       ongoing_session: Session
                                       ) -> Optional[User]:
    user_obj_by_telegram_id = ongoing_session.query(User).filter(
        User.telegram_id == telegram_id).first()

    return user_obj_by_telegram_id


def get_user_obj_with_masters_by_telegram_id(telegram_id: int
                                             ) -> Optional[User]:
    with DBConnection(db_url=db_engine_url) as session:
        user_obj_with_masters_by_tg_id = session.query(User).options(
            joinedload(User.user_masters)).filter(
            User.telegram_id == telegram_id).first()

        return user_obj_with_masters_by_tg_id


def get_user_objs_with_masters_by_tg_id(telegram_ids: list[int]
                                        ) -> Optional[List[User]]:
    with DBConnection(db_url=db_engine_url) as session:
        user_objs_with_masters_by_tg_id = session.query(User).options(
            joinedload(User.user_masters)).filter(
            User.telegram_id.in_(telegram_ids)).all()

        return user_objs_with_masters_by_tg_id
