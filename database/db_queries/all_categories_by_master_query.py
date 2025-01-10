from sqlalchemy.orm import joinedload

from database.db_connection import DBConnection
from database.db_engine_url import db_engine_url

from database.db_models.category_model import Category
from database.db_models.user_model import User


manager = DBConnection(db_url=db_engine_url)


def get_all_categories_by_master_query(telegram_id: int):
    with manager as session:
        user = session.query(User).filter(
            User.telegram_id == telegram_id
        ).first()

        result = session.query(Category).filter(
            Category.category_masters.has(id=user.user_masters.id)
        ).all()

        return result
