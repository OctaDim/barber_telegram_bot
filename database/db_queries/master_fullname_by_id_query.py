from database.db_connection import DBConnection
from database.db_engine_url import db_engine_url
from database.db_models.master_model import Master


def get_master_full_name_by_id(master_id: int):
    with DBConnection(db_url=db_engine_url) as session:
        master_obj = session.query(
            Master).filter(Master.id == master_id).first()

        master_full_name = master_obj.full_name if master_obj else ""
        return master_full_name
