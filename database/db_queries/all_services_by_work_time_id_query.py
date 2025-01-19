from sqlalchemy.orm import joinedload

from database.db_connection import DBConnection
from database.db_engine_url import db_engine_url

from database.db_models.master_model import Master
from database.db_models.work_time_model import WorkTime


def get_all_services_by_work_time_id(work_time_id: int):
    with DBConnection(db_url=db_engine_url) as session:
        work_time_obj = session.query(WorkTime).filter(
            WorkTime.id == work_time_id).first()

        master_obj = session.query(Master).options(
            joinedload(Master.master_services)).filter(
            Master.id == work_time_obj.work_time_masters.id).first()

        services = master_obj.master_services

        return services
