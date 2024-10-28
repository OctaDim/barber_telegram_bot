from database.db_connection import DBConnection
from database.db_engine_url import db_engine_url
from database.db_models.service_model import Service


def get_service_by_id(service_id: int) -> Service:
    with DBConnection(db_url=db_engine_url) as session:
        service_by_id = session.query(
            Service).filter(Service.id == service_id).first()

        return service_by_id
