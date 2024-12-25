from typing import Optional

from database.db_connection import DBConnection
from database.db_engine_url import db_engine_url
from database.db_models.category_model import Category


def get_category_obj_by_id(category_id: int) -> Optional[Category]:
    with DBConnection(db_url=db_engine_url) as session:
        category_by_id = session.query(
            Category).filter(Category.id == category_id).first()

        return category_by_id
