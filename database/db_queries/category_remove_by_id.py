from database.db_connection import DBConnection
from database.db_engine_url import db_engine_url

from database.db_models.category_model import Category
from database.db_utilities.model_object_update import update_object

manager = DBConnection(db_url=db_engine_url)


def remove_category_by_id(category_id: int):
    with manager as session:
        category_obj = session.query(Category).filter(
            Category.id == category_id).first()

        session.delete(category_obj)
        session.commit()
