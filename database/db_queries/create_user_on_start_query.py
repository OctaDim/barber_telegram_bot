from database.db_connection import DBConnection
from database.db_engine_url import db_engine_url

from database.db_models.user_model import User
from database.db_models.user_role_model import UserRole


manager = DBConnection(db_url=db_engine_url)


def create_user_on_start(data: dict, master: bool):
    with manager as session:
        if master:
            role = session.query(UserRole).filter(UserRole.name == 'Master').first()
        else:
            role = session.query(UserRole).filter(UserRole.name == 'User').first()

        valid_data = {
            'telegram_id': data.get('id'),
            'username': data.get('username'),
            'first_name': data.get('first_name'),
            'last_name': data.get('last_name'),
            'birth_date': data.get('birthdate'),
            'role_id': role.id
        }

        session.add(User(**valid_data))
        session.commit()
