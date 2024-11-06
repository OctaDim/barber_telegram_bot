from typing import List

from sqlalchemy.orm import joinedload

from database.db_connection import DBConnection
from database.db_engine_url import db_engine_url
from database.db_models.master_model import Master
from database.db_models.service_model import Service


def get_services_filtered_by_category_master(selected_category_id: int,
                                             selected_master_id: int
                                             ) -> List[Service]:
    with DBConnection(db_url=db_engine_url) as session:
        filtered_services_records = session.query(Service).filter(
            Service.category_id == selected_category_id,
            Service.service_masters.any(Master.id == selected_master_id)
        ).options(
            joinedload(Service.service_masters)
        ).order_by(
            "name", "price"
        ).all()
        return filtered_services_records


def get_services_filtered_by_master(selected_master_id: int
                                    ) -> List[Service]:
    with DBConnection(db_url=db_engine_url) as session:
        filtered_services_records = session.query(Service).filter(
            Service.service_masters.any(Master.id == selected_master_id)
        ).options(
            joinedload(Service.service_masters)
        ).order_by(
            "name", "price"
        ).all()
        return filtered_services_records


def get_services_filtered_by_category(selected_category_id: int
                                      ) -> List[Service]:
    with DBConnection(db_url=db_engine_url) as session:
        filtered_services_records = session.query(Service).filter(
            Service.category_id == selected_category_id,
        ).order_by(
            "name", "price"
        ).all()
        return filtered_services_records
