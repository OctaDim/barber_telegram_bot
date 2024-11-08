from database.db_connection import DBConnection
from database.db_engine_url import db_engine_url
from database.db_models.service_model import Service


def get_masters_full_names_by_service_id(service_id: int):
    with DBConnection(db_url=db_engine_url) as session:
        service_obj = session.query(Service).filter(
            Service.id == service_id).first()

        if service_obj:
            masters_objs = service_obj.service_masters
            if masters_objs:
                names_tuple = tuple(master.full_name for master in masters_objs)
                names_string = ", ".join(names_tuple)
                return names_string
        return ""
