import datetime

from database.db_engine_url import db_engine_url
from database.db_connection import DBConnection
from database.db_utilities.model_object_update import update_object

from database.db_models.services_model import Services


manager = DBConnection(db_url=db_engine_url)


def add_services(data: dict):
    with manager as session:
        validate_data = {
            'name': data['name'],
            'description': data['description'],
            'price': data['price'],
            'time_duration': datetime.time(hour=data['duration_hours'], minute=data['duration_minutes'])
        }

        service = session.query(Services).filter(Services.id == data.get('id_service')).first()

        if service:
            update_object(
                data=validate_data,
                obj=service,
                session=session
            )

            return

        session.add(Services(**validate_data))
        session.commit()

        return


def get_one_service(id_service: int):
    with manager as session:
        data = session.query(Services).filter(Services.id == id_service).first()

        return data


def services_remove(id_service: int):
    with manager as session:
        service = session.query(Services).filter(Services.id == id_service).first()

        session.delete(service)
        session.commit()


get_one_service(17)