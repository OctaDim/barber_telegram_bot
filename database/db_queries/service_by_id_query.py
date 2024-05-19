from database.db_engine_url import db_engine_url
from database.db_connection import DBConnection
from database.db_models.services_model import Services


def get_service_by_id(service_id: int):
    with DBConnection(db_url=db_engine_url) as session:
        service_by_id = session.query(
            Services).filter(Services.id == service_id).first()

        return service_by_id
