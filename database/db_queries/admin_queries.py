import datetime

from database.db_connection import DBConnection
from database.db_engine_url import db_engine_url
from database.db_models.service_model import Service
from database.db_models.category_model import Category
from database.db_queries.user_obj_by_telegram_id import (
    get_user_obj_with_masters_by_telegram_id)
from database.db_utilities.model_object_update import update_object

manager = DBConnection(db_url=db_engine_url)


def add_services(
        data: dict,
        user_telegram_id,
        category_id: int = None
):
    with manager as session:
        user = get_user_obj_with_masters_by_telegram_id(
            telegram_id=user_telegram_id)

        validate_data = {
            'name': data['name'],
            'description': data['description'],
            'price': data['price'],
            'time_duration': datetime.time(hour=data['duration_hours'], minute=data['duration_minutes']),
            'service_masters': [user.user_masters]
        }

        if category_id:
            validate_data['category_id'] = category_id

        service = session.query(Service).filter(
            Service.id == data.get('id_service')).first()

        if service:
            validate_data.pop('service_masters', None)
            update_object(
                data=validate_data,
                obj=service,
                session=session
            )

            return

        session.add(Service(**validate_data))
        session.commit()

        return


def get_one_service(id_service: int):
    with manager as session:
        data = session.query(Service).filter(Service.id == id_service).first()

        return data


def services_remove(id_service: int):
    with manager as session:
        service = session.query(Service).filter(Service.id == id_service).first()

        session.delete(service)
        session.commit()
