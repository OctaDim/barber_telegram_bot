from database.db_connection import DBConnection
from database.db_engine_url import db_engine_url

from database.db_models.category_model import Category
from database.db_models.user_model import User

manager = DBConnection(db_url=db_engine_url)


def create_category_query(name: str, telegram_id: int):
    with manager as session:
        user = session.query(User).filter(
            User.telegram_id == telegram_id
        ).first()

        category = Category(name=name, master_id=user.user_masters.id)

        session.add(category)
        session.commit()

        session.refresh(category)
