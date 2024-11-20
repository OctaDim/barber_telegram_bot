from database.db_connection import DBConnection
from database.db_engine_url import db_engine_url
from database.db_models.reservation_model import Reservation


def get_reservation_obj_by_id(reservation_id: int) -> Reservation:
    with DBConnection(db_url=db_engine_url) as session:
        reservation_obj = session.query(Reservation).filter(
            Reservation.id == reservation_id).first()

    return reservation_obj
