from datetime import datetime

from database.db_engine_url import db_engine_url
from database.db_connection import DBConnection
from database.db_utilities.model_object_update import update_object

from database.db_models.work_time_model import WorkTime

manager = DBConnection(db_url=db_engine_url)


def create_work_time(data: dict):
    with manager as session:
        start_time = data.get('time_start')
        end_time = data.get('time_end')
        delta = data.get('interval')
        year = data.get('year')
        month = data.get('month')
        days: list = data.get('days')

        for day in days:
            base_date = datetime.strptime(f"{year}-{month}-{day}", "%Y-%B-%d")

            session.add(WorkTime(
                start_time=base_date + start_time,
                end_time=base_date + end_time,
                delta=delta
            ))
            session.commit()
