from database.db_models.service_model import Service


def get_masters_names_by_service_obj(service_obj: Service) -> str:
    masters_objs = service_obj.service_masters
    masters_full_names = tuple(master.full_name for master in masters_objs)
    masters_full_names = ", ".join(masters_full_names)
    masters_full_names = "" if not masters_full_names else masters_full_names
    return masters_full_names
