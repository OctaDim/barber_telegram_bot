from random import choice

from database.db_models.services_model import Services

from telegram.params.messages_inserts import MSG
from telegram.params.messages_variants import SERVICE_SELECTED_VARIANTS


def get_service_brief_info_from_record(service_record: Services) -> str:
    service_brief_text = (f"{MSG.SERVICE_NAME}: {service_record.name} - \n"
                          f"{MSG.SERVICE_PRICE}: {service_record.price} {MSG.CURRENCY_BRIEF}  \n"
                          f"{MSG.DURATION}: {service_record.time_duration}")
    return service_brief_text


def get_service_brief_info_from_dict(service_info: dict) -> str:
    service_brief_text = (
        f"{MSG.SERVICE_NAME}: {service_info.get("text")} - \n"
        f"{MSG.SERVICE_PRICE}: {service_info.get("price")}  \n"
        f"{MSG.DURATION}: {service_info.get("duration")}\n")
    return service_brief_text


def get_service_detailed_info(service: Services) -> str:
    service_detailed_text = (f"{choice(SERVICE_SELECTED_VARIANTS)}:\n\n"
                             f"{MSG.SERVICE_NAME}: "
                             f"{service.name}\n"
                             f"{MSG.SERVICE_PRICE}: "
                             f"{service.price} {MSG.CURRENCY_BRIEF}\n"
                             f"{MSG.SERVICE_DURATION}: "
                             f"{service.time_duration}\n"
                             f"{MSG.SERVICE_DESCRIPTION}: {service.description}")

    return service_detailed_text
