from database.db_connection import DBConnection
from database.db_engine_url import db_engine_url
from database.db_models.service_model import Service
from database.db_models.user_model import User
from database.db_models.work_time_model import WorkTime
from database.db_utilities.model_object_update import update_object

manager = DBConnection(db_url=db_engine_url)


def create_service_using_the_master(data: dict):
    with manager as session:
        user_data = {
            'first_name': data.get('first_name'),
            'phone_number': data.get('phone_number')
        }

        user = User(**user_data)

        session.add(user)
        session.commit()

        session.refresh(user)

        service_obj = session.query(Service).filter(Service.id == data.get('service_id')).first()

        work_time_data = {
            'work_time_services': [service_obj],
            'work_time_clients': [user],
            'reserved': True
        }

        work_time_obj = session.query(WorkTime).filter(WorkTime.id == data.get('work_time_id')).first()

        date_day = work_time_obj.time_start

        update_object(data=work_time_data, obj=work_time_obj, session=session)

        return date_day
