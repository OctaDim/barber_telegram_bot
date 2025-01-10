from database.db_connection import DBConnection
from database.db_engine_url import db_engine_url

from database.db_models.category_model import Category
from database.db_utilities.model_object_update import update_object

manager = DBConnection(db_url=db_engine_url)



def category_update_data_query(category_id: id, name: str):
    with manager as session:
        category = session.query(Category).filter(
            Category.id == category_id
        ).first()

        data = {
            'name': name
        }

        update_object(obj=category, session=session, data=data)
